import numpy as np
import hardpotato.potentiostat as pstat
import hardpotato.load_data as load_data
import matplotlib.pyplot as plt

class CPSweep:
    '''
    Batch runner for Chronopotentiometry (CP) experiments.
    Accepts numpy arrays for current and segments to automate multiple runs.
    '''
    def __init__(self, ic_array, ia_array, segments_array, **kwargs):
        self.ic_array = ic_array
        self.ia_array = ia_array
        self.segments_array = segments_array
        self.kwargs = kwargs
        self.results = []

    def run(self):
        '''
        Loop through the arrays and execute experiments.
        '''
        for k in range(len(self.ic_array)):
            ic = self.ic_array[k]
            ia = self.ia_array[k]
            cl = self.segments_array[k]
            fileName = f'CP_{k}'
            
            print(f'Starting experiment {k}: ic={ic}, ia={ia}, cl={cl}')
            
            # Initialize CP technique
            cp = pstat.CP(ic=ic, ia=ia, cl=cl, fileName=fileName, **self.kwargs)
            
            # Run command (generates macro and executes)
            cp.run()
            
            # Load result
            data = load_data.CP(f'{fileName}.txt', pstat.folder_save, pstat.model_pstat)
            self.results.append({'t': data.t, 'E': data.E, 'ic': ic, 'ia': ia, 'cl': cl})
            
        return self.results

    def plot_all(self):
        '''
        Plot all collected results in a single figure.
        '''
        if not self.results:
            print("No results to plot. Run the sweep first.")
            return

        plt.figure(figsize=(10, 6))
        for i, res in enumerate(self.results):
            plt.plot(res['t'], res['E'], label=f'Exp {i}: ic={res["ic"]}A')
        
        plt.xlabel('Time / s')
        plt.ylabel('Potential / V')
        plt.title('CP Batch Sweep Results')
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    # Initial setup example
    # pstat.Setup(model='chi1205b', folder='./data')
    
    ic_vals = np.array([1e-6, 2e-6])
    ia_vals = np.array([0, 0])
    seg_vals = np.array([2, 2])
    
    # cp_sweep = CPSweep(ic_vals, ia_vals, seg_vals)
    # cp_sweep.run()
    # cp_sweep.plot_all()
    pass

if __name__ == '__main__':
    # Example usage:
    # Setup potentiostat first:
    # pstat.Setup(model='chi1205b', path='C:/CHI/chi1205b.exe', folder='C:/Data')
    
    ic_vals = np.array([1e-6, 2e-6, 5e-6])
    ia_vals = np.zeros_like(ic_vals)
    seg_vals = np.ones_like(ic_vals, dtype=int)
    
    # results = run_sweep(ic_vals, ia_vals, seg_vals)
    # plot_all(results)
    pass
