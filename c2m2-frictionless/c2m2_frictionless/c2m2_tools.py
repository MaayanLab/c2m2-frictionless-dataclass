''' Common helper tools for c2m2 instances
'''

def build_term_tables(outdir, ignored_cvs=set(), ignored_categories=set(), cachedir='.cached'):
  ''' Taken from: https://github.com/nih-cfde/cfde-deriva/blob/master/extractors_and_metadata.HMP.Level_1/build_term_tables.py
  Modified to download ontologies from remote and operate in place
  '''
  # TODO: clean up, potentially yield dataclasses instead
  import os
  import json
  import re
  import sys
  import urllib.request
  draftDir = outdir
  cvRefDir = cachedir
  outDir = outdir
  cvFile = {
    'EDAM' : dict(
      remote='https://raw.githubusercontent.com/nih-cfde/cfde-deriva/e924ab292edc3611a25faff92b21935127471b15/extractors_and_metadata.HMP.Level_1/003_external_CVs_versioned_reference_files/EDAM.version_1.21.tsv',
      local='%s/EDAM.version_1.21.tsv' % (cvRefDir),
    ),
    'OBI' : dict(
      remote='https://raw.githubusercontent.com/nih-cfde/cfde-deriva/e924ab292edc3611a25faff92b21935127471b15/extractors_and_metadata.HMP.Level_1/003_external_CVs_versioned_reference_files/OBI.version_2020-08-24.obo',
      local='%s/OBI.version_2020-08-24.obo' % (cvRefDir),
    ),
    'UBERON' : dict(
      remote='https://raw.githubusercontent.com/nih-cfde/cfde-deriva/e924ab292edc3611a25faff92b21935127471b15/extractors_and_metadata.HMP.Level_1/003_external_CVs_versioned_reference_files/uberon.version_2019-06-27.obo',
      local='%s/uberon.version_2019-06-27.obo' % (cvRefDir),
    ),
  }
  targetTSVs = ( 'file.tsv', 'biosample.tsv' )
  termsUsed = {
    'file_format': {},
    'data_type': {},
    'assay_type': {},
    'anatomy': {}
  }
  #
  def fetch_cache_and_open(remote=None, local=None, mode='r'):
    if os.path.exists(local):
      return open(local, mode)
    else:
      os.makedirs(os.path.dirname(local), exist_ok=True)
      urllib.request.urlretrieve(remote, local)
      return open(local, mode)
  #
  def identifyTermsUsed():
    for basename in targetTSVs:
      inFile = draftDir + '/' + basename
      with open( inFile, 'r' ) as IN:
        header = IN.readline()
        colNames = re.split(r'\t', header.rstrip('\r\n'))
        currentColIndex = 0
        columnToCategory = dict()
        for colName in colNames:
          if colName in termsUsed:
            columnToCategory[currentColIndex] = colName
          currentColIndex += 1
        for line in IN:
          fields = re.split(r'\t', line.rstrip('\r\n'))
          for colIndex in columnToCategory:
            currentCategory = columnToCategory[colIndex]
            if fields[colIndex] != '':
              termsUsed[currentCategory][fields[colIndex]] = {}
  #
  def decorateTermsUsed():
    for categoryID in termsUsed:
      if categoryID in ignored_categories:
        continue
      if categoryID == 'anatomy' or categoryID == 'assay_type':
        cv = ''
        if categoryID == 'anatomy':
          cv = 'UBERON'
        elif categoryID == 'assay_type':
          cv = 'OBI'
        if cv in ignored_cvs:
          continue
        with fetch_cache_and_open(**cvFile[cv]) as IN:
          recording = False
          currentTerm = ''
          for line in IN:
            line = line.rstrip('\r\n')
            matchResult = re.search(r'^id:\s+(\S.*)$', line)
            if not( matchResult is None ):
              currentTerm = matchResult.group(1)
              if currentTerm in termsUsed[categoryID]:
                recording = True
                if 'synonyms' not in termsUsed[categoryID][currentTerm]:
                  termsUsed[categoryID][currentTerm]['synonyms'] = ''
              else:
                currentTerm = ''
                # (Recording is already switched off by default.)
            elif not( re.search(r'^\[Term\]', line) is None ):
              recording = False
            elif recording:
              if not ( re.search(r'^name:\s+(\S*.*)$', line) is None ):
                termsUsed[categoryID][currentTerm]['name'] = re.search(r'^name:\s+(\S*.*)$', line).group(1)
              elif not ( re.search(r'^def:\s+\"(.*)\"[^\"]*$', line) is None ):
                termsUsed[categoryID][currentTerm]['description'] = re.search(r'^def:\s+\"(.*)\"[^\"]*$', line).group(1)
              elif not ( re.search(r'^def:\s+', line) is None ):
                raise Exception('Unparsed def-line in %s OBO file: "%s"; aborting.' % (cv, line) )
              elif not ( re.search(r'^synonym:\s+\"(.*)\"[^\"]*$', line) is None ):
                synonym = re.search(r'^synonym:\s+\"(.*)\"[^\"]*$', line).group(1)
                if termsUsed[categoryID][currentTerm]['synonyms'] != '':
                  termsUsed[categoryID][currentTerm]['synonyms'] = termsUsed[categoryID][currentTerm]['synonyms'] + '|' + synonym
                else:
                  termsUsed[categoryID][currentTerm]['synonyms'] = synonym
      elif categoryID == 'file_format' or categoryID == 'data_type':
        cv = 'EDAM'
        if cv in ignored_cvs:
          continue
        with fetch_cache_and_open(**cvFile[cv]) as IN:
          header = IN.readline()
          for line in IN:
            line = line.rstrip('\r\n')
            ( termURL, name, synonyms, definition ) = re.split(r'\t', line)[0:4]
            currentTerm = re.sub(r'^.*\/([^\/]+)$', r'\1', termURL)
            currentTerm = re.sub(r'data_', r'data:', currentTerm)
            currentTerm = re.sub(r'format_', r'format:', currentTerm)
            if currentTerm in termsUsed[categoryID]:
              # There are some truly screwy things allowed inside
              # tab-separated fields in this file. Clean them up.
              name = name.strip().strip('"\'').strip()
              synonyms = synonyms.strip().strip('"\'').strip()
              definition = definition.strip().strip('"\'').strip()
              definition = re.sub( r'\|.*$', r'', definition )
              termsUsed[categoryID][currentTerm]['name'] = name
              termsUsed[categoryID][currentTerm]['description'] = definition
              termsUsed[categoryID][currentTerm]['synonyms'] = synonyms
  #
  def writeTermsUsed():
    for categoryID in termsUsed:
      if categoryID in ignored_categories:
        continue
      outFile = '%s/%s.tsv' % (outDir, categoryID)
      with open(outFile, 'w') as OUT:
        OUT.write( '\t'.join( [ 'id', 'name', 'description', 'synonyms' ] ) + '\n' )
        for termID in termsUsed[categoryID]:
          try:
            #OUT.write( '\t'.join( [ termID, termsUsed[categoryID][termID]['name'], termsUsed[categoryID][termID]['description'], termsUsed[categoryID][termID]['synonyms'] ] ) + '\n' )
            # The synonyms we loaded from the OBO files don't conform to the spec constraints. Punting to blank values for now.
            OUT.write( '\t'.join( [ termID, termsUsed[categoryID][termID]['name'], termsUsed[categoryID][termID]['description'], ''] ) + '\n' )
          except:
            import traceback; traceback.print_exc(file=sys.stderr)
            import ipdb; ipdb.post_mortem(sys.exc_info()[2])
  #
  if not os.path.isdir(outDir) and os.path.exists(outDir):
    raise Exception('%s exists but is not a directory aborting.' % (outDir))
  elif not os.path.isdir(outDir):
    os.mkdir(outDir)
  #
  identifyTermsUsed()
  decorateTermsUsed()
  writeTermsUsed()

def build_term_tables_taxon(outdir):
  import os
  import re
  import time
  import csv
  import xml.etree.ElementTree
  import urllib.request
  def ncbi_taxon_fetch(id):
    T = xml.etree.ElementTree.parse(
      urllib.request.urlopen(
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id={id}"
      )
    )
    time.sleep(0.1)
    t = T.find('Taxon')
    return {
      'id': t.find('TaxId').text.strip(),
      'name': t.find('ScientificName').text.strip(),
      'synonyms': t.find('OtherNames').text.strip(),
      'rank': t.find('Rank').text.strip(),
    }
  #
  txid_matcher = re.compile(r'NCBI:txid(\d+)$')
  txids = set()
  # get NCBI tax ids in use
  with open(os.path.join(outdir, 'subject_role_taxonomy.tsv'), 'r') as fr:
    reader = csv.reader(fr, delimiter='\t')
    header = next(reader)
    for row in reader:
      row = dict(zip(header, row))
      m = txid_matcher.match(row['taxonomy_id'])
      if m:
        txids.add(m.group(1))
  
  with open(os.path.join(outdir, 'ncbi_taxonomy.tsv'), 'w') as fw:
    writer = csv.writer(fw, delimiter='\t')
    writer.writerow(['id', 'clade', 'name', 'description', 'synonyms'])
    for txid in txids:
      taxon = ncbi_taxon_fetch(txid)
      assert str(txid) == taxon['id']
      writer.writerow([
        f"NCBI:txid{txid}",
        taxon['rank'],
        taxon['name'],
        '',
        taxon['synonyms'],
      ])

def validate_id_namespace_name_uniqueness(pkg):
  import json
  from collections import Counter
  for rc in pkg.resources:
    print(f"Checking {rc.name} id_namespace name uniqueness...")
    # count id_namespace_name_pairs
    id_namespace_name_pairs = Counter()
    for record in rc.read(keyed=True):
      if 'id_namespace' in record and 'name' in record:
        id_namespace_name_pairs.update({(record['id_namespace'], record['name']): 1})
    # enumerate the duplicates
    duplicates = sorted([
      (count, id_namespace, name)
      for (id_namespace, name), count in id_namespace_name_pairs.items()
      if count > 1
    ], reverse=True)
    assert duplicates == [], f"Duplicate id_namespace, name pairs found in {rc.name}: {json.dumps(duplicates)}"
