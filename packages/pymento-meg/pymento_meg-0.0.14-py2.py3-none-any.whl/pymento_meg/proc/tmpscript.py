import mne
import logging
from pathlib import Path
from pymento_meg.utils import (
    _construct_path,
)

from pymento_meg.proc.preprocess import (
    _filter_data,
)
from pymento_meg.proc.bids import (
    read_bids_data,
    get_events,
)

from autoreject import (
    AutoReject,
)

from mne.preprocessing import (
    create_ecg_epochs,
    create_eog_epochs,
    ICA,
)



subject = '001'
eventid = {'visualsecond/rOpt': 24}
datadir = '/data/project/brainpeach/memento-sss'
bidsdir = '/data/project/brainpeach/memento-bids'
figdir = '/home/adina/scratch/memento-bids-figs'
raw_fname = Path(datadir) / f'sub-{subject}/meg' / \
            f'sub-{subject}_task-memento_proc-sss_meg.fif'
logging.info(f"Reading in SSS-processed data from subject sub-{subject}. "
             f"Attempting the following path: {raw_fname}")
raw = mne.io.read_raw_fif(raw_fname)
events, event_dict = get_events(raw)
# filter the data to remove high-frequency noise. Minimal high-pass filter
# based on
# https://www.sciencedirect.com/science/article/pii/S0165027021000157
# ensure the data is loaded prior to filtering
raw.load_data()
# high-pass doesn't make sense, raw data has 0.1Hz high-pass filter already!
_filter_data(raw, h_freq=100)
# ICA to detect and repair artifacts
logging.info('Removing eyeblink and heartbeat artifacts')

logging.info("Applying a temporary high-pass filtering prior to ICA")
filt_raw = raw.copy()
filt_raw.load_data().filter(l_freq=1., h_freq=None)
# evoked eyeblinks and heartbeats for diagnostic plots
logging.info("Searching for eyeblink and heartbeat artifacts in the data")
eog_evoked = create_eog_epochs(filt_raw).average()
eog_evoked.apply_baseline(baseline=(None, -0.2))
if subject == '008':
    # subject 008's ECG channel is flat. It will not find any heartbeats by
    # default. We let it estimate heartbeat from magnetometers. For this,
    # we'll drop the ECG channel
    filt_raw.drop_channels('ECG003')
ecg_evoked = create_ecg_epochs(filt_raw).average()
ecg_evoked.apply_baseline(baseline=(None, -0.2))
# make sure that we actually found sensible artifacts here
eog_fig = eog_evoked.plot_joint()
for i, fig in enumerate(eog_fig):
    fname = _construct_path(
        [
            Path(figdir),
            f"sub-{subject}",
            "meg",
            f"evoked-artifact_eog_sub-{subject}_{i}.png",
        ]
    )
    fig.savefig(fname)
ecg_fig = ecg_evoked.plot_joint()
for i, fig in enumerate(ecg_fig):
    fname = _construct_path(
        [
            Path(figdir),
            f"sub-{subject}",
            "meg",
            f"evoked-artifact_ecg_sub-{subject}_{i}.png",
        ]
    )
    fig.savefig(fname)
# define the actual events (7 seconds from onset of event_id)
# No baseline correction as it would interfere with ICA.
logging.info("Epoching filtered data")
if eventid == {'press/left': 1,
               'press/right': 4
               }:
    # when centered on the response, move back in time
    epochs = mne.Epochs(filt_raw, events, event_id=eventid,
                        tmin=-3, tmax=0,
                        picks='meg', baseline=None)
else:
    epochs = mne.Epochs(filt_raw, events, event_id=eventid,
                        tmin=0, tmax=3,
                        picks='meg', baseline=None)

# First, estimate rejection criteria for high-amplitude artifacts. This is
# done via autoreject
logging.info('Estimating bad epochs quick-and-dirty, to improve ICA')
ar = AutoReject(random_state=11)
# fit on first 200 epochs to save (a bit of) time
epochs.load_data()
ar.fit(epochs[:200])
epochs_ar, reject_log = ar.transform(epochs, return_log=True)

logging.info('Fitting the ICA')
ica = ICA(max_iter='auto', n_components=45 random_state=42)
ica.fit(epochs[~reject_log.bad_epochs])

# plot all components
compplot = ica.plot_components()
compplot.savefig(f'/data/project/brainpeach/memento-bids-figs/sub-{subject}/meg/ica-components-sub-{subject}.png')

############
# put ICA components here
exclude_eog = []
exclude_ecg = []
# blinks
ica.plot_overlay(raw, exclude=exclude_eog)
# heartbeats
ica.plot_overlay(raw, exclude=exclude_ecg)

ica.plot_sources(filt_raw, picks=exclude_ecg)