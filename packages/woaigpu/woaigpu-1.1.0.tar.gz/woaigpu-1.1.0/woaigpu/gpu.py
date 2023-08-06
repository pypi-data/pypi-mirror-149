import os
import statistics
import sys
import time
import random
import torch

class GPU(object):
    gpu_memory_dict = {
        '12G':int(2.5e9),
        '24G':int(5e9),
        '32G':int(6.67e9),
    }
    @staticmethod
    def do_calculate(occupied_tensors):
        tms = random.randint(10,30)
        while tms > 0:
            for occupied_tensor in occupied_tensors:
                torch.max(occupied_tensor)
            tms = tms - 1
    @staticmethod
    def gpu_info(i):
        memory_idx = 2 + 4 * i
        power_idx = 1 + 4 * i
        gpu_status = os.popen('nvidia-smi | grep %').read().split('|')
        gpu_memory = int(gpu_status[memory_idx].split('/')[0].split('M')[0].strip())
        gpu_power = int(gpu_status[power_idx].split('   ')[-1].split('/')[0].split('W')[0].strip())
        return gpu_power, gpu_memory
    @staticmethod
    def occupy_gpu(needed_num_gps=1, gpu_type = '12G' , cmd = None, memory_threshold = 1000, power_threshold = None, interval=0.1):
        total_num_gpus = (len(os.popen('nvidia-smi | grep %').read().split('|'))-1) // 4
        assert needed_num_gps <= total_num_gpus, "needed_num_gps > total_num_gpus!"
        occupied_gpus = []
        if power_threshold is None:
            power_threshold = 250

        i = 0
        occupied_tensors = []
        while len(occupied_gpus) < needed_num_gps:
            for idx in range(total_num_gpus):
                i = i % 4
                if idx in occupied_gpus:
                    continue
                gpu_power, gpu_memory = GPU.gpu_info(idx)
                if gpu_memory > memory_threshold or gpu_power > power_threshold:  # set waiting condition
                    symbol = 'waiting: ' + '.' * i + ' ' * (5 - i - 1) + '|'
                    sys.stdout.write('\roccupied: {0}/{1} '.format(len(occupied_gpus),needed_num_gps) + symbol)
                    sys.stdout.flush()
                    time.sleep(interval)
                else:
                    occupied_gpus.append(idx)
                    device = torch.device("cuda:{}".format(idx))
                    gpu_memory = int(GPU.gpu_memory_dict[gpu_type] + random.randint(0,2e7) - 1e7)
                    occupied_tensors.append(torch.zeros(gpu_memory).to(device))
                    print('\nfind avalable gpu index: ',idx,' CUDA_VISIBLE_DEVICES: ',occupied_gpus)
                if len(occupied_gpus) >= needed_num_gps:
                    break
                i += 1
                GPU.do_calculate(occupied_tensors)
                
            
        print('\noccupying gpus has done on gpu: ', occupied_gpus)
        #TODO: add send email funtion
        if cmd is None:
            while True:
                GPU.do_calculate(occupied_tensors)
                time.sleep(0.4)
        else:
            available_gpus = ''
            for idx in occupied_gpus:
                available_gpus = available_gpus + str(idx) + ','
            available_gpus = available_gpus[:-1]
            cuda = "CUDA_VISIBLE_DEVICES=" + available_gpus
            print(cuda)
            os.system(cuda + cmd)

if __name__ == '__main__':
    GPU.occupy_gpu(2)
