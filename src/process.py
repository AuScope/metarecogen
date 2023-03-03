STATES = { 'vic': { 'method': 'PDF',
                    'params': { 'URLS': [ ] }
				  },
           'tas':  { 'method': 'PDF',
		             'params': { 'URLS': [ ] }
				  },
		   'nsw' : { 'method': None },
		   'ga': { 'method': None },
		   'qld': { 'method': 'CKAN',
		            'params': { 'URL': 'https://dffgg.ggfgf/api' }
				  },
		    'sa': { 'method': 'ISO19139',
			        'params': { 'URL': 'https://dffgg.ggfgf/api' }
				  },
			'nt':  { 'method': 'PDF',
		             'params': { 'URLS': [ ] }
				  },
			'wa': { 'method': 'ISO19139',
			        'params': { 'URLS': [ ] }
				   }
		}
		

if __name__ == "__main__":
    for k,v in STATES.items():
	    if v['method'] == 'PDF':
		    pdf_convert(k, v['params'])
		elif v['method'] == 'CKAN':
		    pdf_convert(k, v['params'])
		elif v['method'] == 'ISO19139':
		    pdf_convert(k, v['params'])

		
