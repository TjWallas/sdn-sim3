import os
from of_dev_instances.executesim import execute_sim
import of_dev_instances.config as cfg
import of_dev_instances.sim_flow_info_read as f_info
import of_dev_instances.sim_flow_meter_read as f_meter
from of_dev_instances.of_volumetric_attribute_writer import OFVolumetricAttributeWriter

# files = ['17-01-01','17-01-02','17-01-03','17-01-04','17-01-05','17-01-06','17-01-07','17-01-08','17-01-09','17-01-10','17-01-11','17-01-12','17-01-13','17-01-14','17-01-16','17-01-17','17-01-18','17-01-19','17-01-20','17-01-21','17-01-22','17-01-23','17-01-24','17-01-25','17-01-26','17-01-27','17-01-28','17-01-29','17-01-30','17-01-31']
files = ['16-12-17','16-12-18','16-12-19','16-12-20','16-12-21','16-12-22','16-12-23','16-12-24','16-12-25','16-12-26','16-12-27','16-12-29','16-12-30','16-12-31','17-01-01','17-01-02','17-01-03','17-01-04','17-01-05','17-01-06','17-01-07','17-01-08','17-01-09','17-01-10','17-01-11','17-01-12','17-01-13','17-01-14','17-01-16','17-01-17','17-01-18','17-01-19','17-01-20','17-01-21','17-01-22','17-01-23','17-01-24','17-01-25','17-01-26','17-01-27','17-01-28','17-01-29','17-01-30','17-01-31','17-02-01','17-02-03','17-02-04','17-02-05','17-02-06','17-02-07','17-02-08','17-02-09','17-02-10','17-02-11','17-02-12','17-02-13','17-02-14','17-02-15','17-02-16','17-02-17','17-02-18','17-02-19','16-10-17','16-11-04','16-11-22','16-12-10','16-12-28','17-01-15','17-02-02','17-02-20','17-03-10','17-02-21','17-02-22','17-02-23','17-02-24','17-02-25','17-02-26','17-02-27','17-02-28','17-03-01','17-03-02','17-03-03','17-03-04','17-03-05','17-03-06','17-03-07','17-03-08','17-03-09','17-03-11','17-03-12','17-03-13','17-03-14','17-03-15','17-03-16','17-03-17','17-03-18','17-03-19','17-03-20','17-03-21','17-03-22','17-03-23','17-03-24','17-03-25','17-03-26','17-03-27','17-03-28','17-03-29','17-03-30','17-03-31','17-04-01','17-04-02','17-04-03','17-04-04','17-04-05','17-04-06','17-04-07','17-04-08','17-04-09','17-04-10','17-04-11','17-04-12','17-04-13']
# files = ['16-10-01','16-10-02','16-10-03','16-10-04','16-10-05','16-10-06','16-10-07','16-10-08','16-10-09','16-10-10','16-10-11','16-10-12','16-10-13','16-10-14','16-10-15','16-10-16','16-10-18','16-10-19','16-10-20','16-10-21','16-10-22','16-10-23','16-10-24','16-10-25','16-10-26','16-10-27','16-10-28','16-10-29','16-10-30','16-10-31','16-11-01','16-11-02','16-11-03','16-11-05','16-11-06','16-11-07','16-11-08','16-11-09','16-11-10','16-11-11','16-11-12','16-11-13','16-11-14','16-11-15','16-11-16','16-11-17','16-11-18','16-11-19','16-11-20','16-11-21','16-11-23','16-11-24','16-11-25','16-11-26','16-11-27','16-11-28','16-11-29','16-11-30','16-12-01','16-12-02','16-12-03','16-12-04','16-12-05','16-12-06','16-12-07','16-12-08','16-12-09','16-12-11','16-12-12','16-12-13','16-12-14','16-12-15','16-12-16','16-12-17','16-12-18','16-12-19','16-12-20','16-12-21','16-12-22','16-12-23','16-12-24','16-12-25','16-12-26','16-12-27','16-12-29','16-12-30','16-12-31','17-01-01','17-01-02','17-01-03','17-01-04','17-01-05','17-01-06','17-01-07','17-01-08','17-01-09','17-01-10','17-01-11','17-01-12','17-01-13','17-01-14','17-01-16','17-01-17','17-01-18','17-01-19','17-01-20','17-01-21','17-01-22','17-01-23','17-01-24','17-01-25','17-01-26','17-01-27','17-01-28','17-01-29','17-01-30','17-01-31','17-02-01','17-02-03','17-02-04','17-02-05','17-02-06','17-02-07','17-02-08','17-02-09','17-02-10','17-02-11','17-02-12','17-02-13','17-02-14','17-02-15','17-02-16','17-02-17','17-02-18','17-02-19','16-10-17','16-11-04','16-11-22','16-12-10','16-12-28','17-01-15','17-02-02','17-02-20','17-03-10','17-02-21','17-02-22','17-02-23','17-02-24','17-02-25','17-02-26','17-02-27','17-02-28','17-03-01','17-03-02','17-03-03','17-03-04','17-03-05','17-03-06','17-03-07','17-03-08','17-03-09','17-03-11','17-03-12','17-03-13','17-03-14','17-03-15','17-03-16','17-03-17','17-03-18','17-03-19','17-03-20','17-03-21','17-03-22','17-03-23','17-03-24','17-03-25','17-03-26','17-03-27','17-03-28','17-03-29','17-03-30','17-03-31','17-04-01','17-04-02','17-04-03','17-04-04','17-04-05','17-04-06','17-04-07','17-04-08','17-04-09','17-04-10','17-04-11','17-04-12','17-04-13']


def read_volumetric_attributes(config_dict):
    instance_out_file = config_dict['instance_out_file']
    flow_info_file = config_dict['flow_info_file']
    device_info =config_dict['device_info']
    gateway_mac = config_dict['gateway']
    flow_meter_rate_file =config_dict['flow_meter_rate_file']
    flow_meter_count_file =config_dict['flow_meter_count_file']
    attribute_info = config_dict['attribute_info']
    tcam_rules_gen_function = config_dict['tcam_rules_gen_function']

    flow_info = f_info.FlowInfoReader(flow_info_file)

    attribute_writer = OFVolumetricAttributeWriter(instance_out_file,attribute_info)

    for e_device in device_info:
        print(e_device['class'])
        dev_flows = flow_info.find_device_flows(tcam_rules_gen_function(e_device['mac'], gateway_mac))
        attribute_writer.flow_info_dict = dev_flows
        attribute_writer.device_class = e_device['class']

        flow_meter = f_meter.FlowMeterReader(flow_meter_rate_file, flow_meter_count_file)

        for tid, dict_rate, dict_count in flow_meter:
            attribute_writer.put_reading(tid,dict_rate,dict_count)

if __name__ == '__main__':


    for e_f in files:
        print(e_f)
        execute_sim('/Volumes/iot_backup/Ayyoob/pcap/training/24hour/%s.pcap' % e_f)

        read_vol_attributes_config = {
            'instance_out_file': os.path.join(cfg.INSTANCE_OUTPUT_DIR, '%s.csv'%e_f),
            'flow_info_file': cfg.FLOW_INFO_FILE,
            'device_info': cfg.DEVICE_DICT,
            'gateway':cfg.GATE_WAY,
            'flow_meter_rate_file': cfg.FLOW_METER_RATE_FILE,
            'flow_meter_count_file': cfg.FLOW_METER_COUNT_FILE,
            'attribute_info': cfg.BUFFER,
            'tcam_rules_gen_function':cfg.tcam_rules
        }
        read_volumetric_attributes(read_vol_attributes_config)



        # print (dict_rate)