import json
import pandas as pd
from numpy import arange
from StaticEplusEngine import run_eplus_model, convert_json_idf

class EplusOptimization:
    def __init__(self):
        self.eplus_exe_path = './energyplus9.5/energyplus'  # Energyplus executable file path
        self.eplus_idf_model_path = './1ZoneUncontrolled_win_1.idf'  # Energyplus model file path
        self.res_dir = './result1'  # Simulation result directory
        self.eplus_epjson_model_path = './1ZoneUncontrolled_win_1.epJSON'  # Energyplus model file path

        # init the highest indoor air temperature as None
        self.highest_temp = None
        self.optimal_para = (float, float)  # : (shgc,u_factor)
        # convert idf to epJSON
        convert_json_idf(self.eplus_exe_path, self.eplus_idf_model_path)
        pass

    def modify_para(self, shgc, u_factor):
        # Opening JSON file
        with open(self.eplus_epjson_model_path) as epjson:
            epjson_dict = json.load(epjson)
        # modify shgc
        epjson_dict['WindowMaterial:SimpleGlazingSystem']['SimpleWindow:DOUBLE PANE WINDOW'][
            'solar_heat_gain_coefficient'] = shgc
        # modify u_factor
        epjson_dict['WindowMaterial:SimpleGlazingSystem']['SimpleWindow:DOUBLE PANE WINDOW']['u_factor'] = u_factor
        # write JSON file back to file
        with open(self.eplus_epjson_model_path, 'w') as epjson:
            json.dump(epjson_dict, epjson)

    def run_model(self):
        run_eplus_model(self.eplus_exe_path, self.eplus_epjson_model_path, self.res_dir)

    def update_highest(self, shgc, u_factor):
        df = pd.read_csv(self.res_dir + '/eplusout.csv')
        # select column represent the indoor air temperature
        col = df['ZN001:WALL001:WIN001:Surface Inside Face Temperature [C](TimeStep)']
        avg_value = col.mean()
        if not self.highest_temp:
            self.highest_temp = avg_value
            self.optimal_para = (shgc, u_factor)
        elif avg_value > self.highest_temp:
            self.highest_temp = avg_value
            self.optimal_para = (shgc, u_factor)


    def show_optimal_para(self):
        shgc = self.optimal_para[0]
        u_factor = self.optimal_para[1]
        print(f'The highest average indoor air temperature : {self.highest_temp}')
        print(f'Optimal shgc : {shgc}')
        print(f'Optimal u_factor : {u_factor}')

    def main(self):

        for shgc in arange(0.25, 0.76, 0.1):
            shgc = round(shgc, 2)
            for u_factor in arange(1.00, 2.60, 0.1):
                u_factor = round(u_factor, 2)
                self.modify_para(shgc=shgc, u_factor=u_factor)
                self.run_model()
                self.update_highest(shgc=shgc, u_factor=u_factor)
        self.show_optimal_para()

if __name__ == '__main__':
    epo = EplusOptimization()
    epo.main()
