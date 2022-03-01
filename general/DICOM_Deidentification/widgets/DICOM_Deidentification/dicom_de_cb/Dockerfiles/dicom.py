'''
Created on Jan 29, 2022

@author: varikmp
'''

from os.path import splitext
from pydicom import dcmread

DEFAULT_DEIDENTIFIED_FIELDS = ['PatientID', 'PatientName', 'PatientSex', 'PatientBirthDate', 'PatientOrientation']

def de_identify(input_file, fields=DEFAULT_DEIDENTIFIED_FIELDS, output_file=None):
    ds = dcmread(input_file)
    for field in fields:
        setattr(ds, field, None)
    if output_file is None:
        input_file_name, input_file_ext = splitext(input_file)
        output_file = "{}_deidentified{}".format(input_file_name, input_file_ext)
    ds.save_as(output_file)
# de_identify('/home/thesis/workspace/docker/idc/dicom/dcm_sm/lossyJPEG-RGB.dcm')