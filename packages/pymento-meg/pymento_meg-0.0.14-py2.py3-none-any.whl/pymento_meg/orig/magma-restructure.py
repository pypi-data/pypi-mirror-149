import mne
import logging

import os
import os.path as op

from mne_bids import (
    write_raw_bids,
    BIDSPath,
)
from pathlib import Path
from glob import glob

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def read_data_original(
        subject,
        directory='/data/project/magma/magma/data/MEG',
):
    """
    Read in MAGMA raw data for restructuring. Each participant has one
    magma<sub> directory. Within this directory, a BTI system folder structure
    exists, with acquisition name (demos), acquisition time, and session (1)
    directory. In there, a raw data file ('c,rfDC'), a config ('config') file,
    and the digitizer data ('hs_file') are the most important files,
    and MUST be in the same directory.

    magma01                               # sub identifier
    ├── demos                             # acquisition name
    │   ├── 05@-05@-14@_10:45             # acquisition time
    │   │   ├── 1                         # session identifier (no runs)
    │   │   │   ├── config                # config file, acq. info & metadata
    │   │   │   ├── c,rfDC                # raw data, continuously (c) recorded, not filtered (rfDC)
    │   │   │   ├── e,rfhp1.0Hz,COH       # epoched (e) data, 1Hz highpass filter (rfhp1.0Hz), with recording of Coils On Head position (COH)
    │   │   │   ├── e,rfhp1.0Hz,COH1      # epoched (e) data, 1Hz highpass filter (rfhp1.0Hz), with recording of Coils On Head position (COH)
    │   │   │   ├── Exp~c,rfDC
    │   │   │   ├── Exp~e,rfhp1.0Hz,COH
    │   │   │   ├── Exp~e,rfhp1.0Hz,COH1
    │   │   │   └── hs_file               # digitizer data, digitized head-shape coordinates (x, y, z points)
    │   │   └── Exp~1
    │   └── Exp~05@-05@-14@_10:45
    └── Exp~demos

    binary Exp~* files are residue (?) Luca says the scanner creates them
    As BTi/4D files do not have uniquely identifiable names over subjects, each
    subjects' file names are identical. BIDS MEG specifies to keep them in a
    dedicated directory (https://bids-specification.readthedocs.io/en/stable/99-appendices/06-meg-file-formats.html#bti4d-neuroimaging)

    If needed, we save the raw data in a BIDS compliant way.
    :param directory: path to a subject directory.
    :param subject: str, subject identifier ('01'), used for file names
     and logging
    :param savetonewdir: Boolean, if True, save the data as BIDS conform
    files into a new directory using mnebids
    :param bidsdir: str, Path to where BIDS conform data shall be saved
    :param preprocessing: Data flavour to load. Existing directories are
     'Move_correc_SSS_realigneddefault_nonfittoiso' and 'Raw' (default)
     :param fine_cal_file: str, path to fine_cal file
     :param figdir: str, path to directory for diagnostic plots
     :param crosstalk_file; str, path to crosstalk file
    :return:
    """

    # We're starting with the original data from Luca. The files were
    # transferred from Hilbert as is. First, construct a Path to the Raw data
    assert op.isdir(directory)
    subject_directory = Path(directory) / f"magma{subject}" / "demos/*/1"
    # there are individual acquisition times for each subject, we need to glob
    globbed_directory = glob(str(subject_directory))[0]
    assert op.exists(globbed_directory)
    # Because mne can't handle Path objects, they need to be strings
    pdf_fname = str(Path(globbed_directory) / 'c,rfDC')
    config = str(Path(globbed_directory) / 'config')
    hs_file = str(Path(globbed_directory) / 'hs_file')
    logging.info(
        f"Reading files for subject sub-{subject} from {globbed_directory}."
    )
    # load the raw data, rename the channels and convert to Neuromag coordinates
    raw = mne.io.read_raw_bti(
        pdf_fname,
        config,
        hs_file,
        convert=False,
        eog_ch=('RVEOGo-1', 'RHEOG-1', 'RVEOGu-1', 'LHEOG-1'),
        ecg_ch=None
        )
    return raw


def save_bids_data(raw, bidsdir, sub):
    """
    Save raw MEG data into a BIDS conform directory
    :param raw:
    :param bidsdir:
    :return:
    """
    # requires renamed channels
    events = mne.find_events(raw, stim_channel=['STI 014'], shortest_event=1)
    # remove events that are known to be spurious.
    exclusion_list = [104, 191, 16504, 16514, 16524, 16534, 16544, 16554, 16564,
                      16574, 16584]
    events = mne.pick_events(events, exclude=exclusion_list)
    event_id = {"message": 100, "fixcross": 120, "option/left": 130, "or": 140,
                "option/right": 150, "responsewindow": 160, "choice/right": 170,
                "choice/left":  180, "reward/yes": 190, "reward/no": 200}
    bids_path = BIDSPath(subject=sub,
                         task='magma',
                         root=bidsdir,
                         datatype='meg')
    if not op.exists(bids_path.directory):
        import os
        os.makedirs(bids_path.directory)
    raw.info['line_freq'] = 50
    raw.info['bads'] = bads[sub]

    logging.info(f"Writing BIDSified data of sub-{sub} to {bids_path}")
    write_raw_bids(raw, bids_path=bids_path, events_data=events,
                   event_id=event_id, overwrite=True)


def restructure(directory, bidsdir):
    """Restructure magma data"""
    for subject in bads.keys():
        if subject.startswith('0') or subject.startswith('1'):
            continue
        raw = read_data_original(subject, directory)
        save_bids_data(raw, bidsdir, subject)


bads = {
    '01': ['A156', 'A142', 'A7'],
    '02': ['A7', 'A142', 'A156', 'A213'],
    '03': ['A7', 'A41', 'A142', 'A156'],
    '04': ['A7', 'A142', 'A156'],
    '05': ['A7', 'A143', 'A142', 'A156'],
    '06': ['A7', 'A142', 'A156', 'A213', 'A154'],
    '07': ['A7', 'A41', 'A142', 'A156', 'A213', 'A135'],
    '08': ['A7', 'A41', 'A142', 'A154', 'A156'],
    '09': ['A7', 'A142', 'A156', 'A235', 'A238', 'A239', 'A236', 'A237', 'A218', 'A219', 'A202', 'A41', 'A164', 'A185', 'A204', 'A213', 'A203'],
    '10': ['A7', 'A142', 'A213'],
    '11': ['A7', 'A41', 'A142', 'A156', 'A154', 'A213'],
    '12': ['A7', 'A142', 'A156', 'A213'],
    '13': ['A7', 'A142', 'A156'],
    '14': ['A7', 'A142', 'A156', 'A213'],
    '15': ['A7', 'A142', 'A156', 'A213'],
    '16': ['A7', 'A41', 'A142', 'A156', 'A219', 'A213'],
    '17': ['A7', 'A142', 'A156'],
    '18': ['A7', 'A142', 'A156', 'A229', 'A230', 'A231'],
    '19': ['A7', 'A142', 'A156'],
    '20': ['A7', 'A142', 'A156'],
    '21': ['A7', 'A142', 'A156'],
    '22': ['A7', 'A142', 'A156'],
    '23': ['A7', 'A142', 'A156'],
    '24': ['A7', 'A142', 'A156'],
    '26': ['A7', 'A142', 'A156'],
    '27': ['A7', 'A142', 'A156'],
    '28': ['A7', 'A142', 'A156'],
    '29': ['A7', 'A142', 'A156', 'A213'],
    '30': ['A7', 'A156', 'A142'],
    '31': ['A7', 'A156', 'A142'],
    '32': ['A7', 'A142', 'A156', 'A213'],
    '33': ['A7', 'A142', 'A156', 'A164'],
    '34': ['A7', 'A142', 'A156'],
    '35': ['A7', 'A142', 'A156'],
    '38': ['A7', 'A142', 'A156']
}

