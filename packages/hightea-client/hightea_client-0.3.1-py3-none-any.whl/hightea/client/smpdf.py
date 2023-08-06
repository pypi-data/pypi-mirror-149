    def write_SMPDFinput(self,directory:str):
        """Write data in format suitable for the SMPDF method

        It is assumed that each histogram contains a full variation
        for the same PDF but for different observables. The header files
        contain some standard parameters which might be adapted by the user.
        A directory as specified is created.

        Parameters
        ----------
        directory: str
            Path specifing the output directory.
        """
        Path(directory).mkdir(parents=True, exist_ok=True)

        res = self.result()

        f_bin = "{:.5g}"

        with open(directory+'/'+self.name+'-runcard.yaml','w') as fp:
            fp.write('smpdf_nonlinear_correction: False\n')
            fp.write('smpdf_tolerance: 0.15\n')
            fp.write('smpdfname: '+res[0]['info']['pdf']+'_'
                                  +self.proc.replace('processes/','')+'_smpdf\n')
            fp.write('order: <ORDER>\n')
            fp.write('pdfsets:\n')
            fp.write('    - '+res[0]['info']['pdf']+'\n')
            fp.write('observables:\n')
            for resi in res:
                obs_string = self.name+'_'
                for it, var in enumerate(resi['info']['binning']):
                    obs_string += var['variable']
                    if it != len(resi['info']['binning'])-1:
                        obs_string += '_X_'
                fp.write('    - '+obs_string+'.yaml\n')
                with open(directory+'/'+obs_string+'.yaml','w') as fpop:
                    fpop.write('#'+obs_string+'\n')
                    fpop.write('nbins: '+str(len(resi['histogram']))+'\n')
                    fpop.write('energy_scale: <ENERGYSCALE>\n')
                    fpop.write('order: <ORDER>\n')
                    fpop.write('pdf_predictions:\n')
                    fpop.write('    '+resi['info']['pdf']+': '+obs_string+'.csv\n')
                with open(directory+'/'+obs_string+'.csv','w') as fpop:
                    line = ''
                    for it in range(0,len(resi['histogram'])):
                        line += '\t'+str(it)
                    fpop.write(line+'\n')
                    n_members = len(resi['histogram'][0]['mean'])
                    for it in range(0,n_members):
                        line = str(it)
                        for jt in range(0,len(resi['histogram'])):
                            line += '\t'+f_bin.format(
                                resi['histogram'][jt]['mean'][it])
                        fpop.write(line+'\n')
            fp.write('actions:\n')
            fp.write('    - smpdf')
