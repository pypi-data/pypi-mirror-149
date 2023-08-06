#!/usr/bin/env python3
from astropy.io import fits as pf
import numpy as np
import click
import logging
from time import gmtime, strftime

# filename1 = 'soft.lc'
# filename2 = 'hard.lc'
# filename3 = 'hratio.qdp'
# min_sn = 10.
# max_time = 1e4
# gti_threshold = 100.
# flag_rebin = 1
# min_bin_size = 0
# ext_t0 = 0
# display_unit = 's'  # {"s", "h", "d"};
# max_point_sn = 100
# single_point_check = False

import sys


file_handler = logging.FileHandler(filename='hratio_%s.log' % (strftime("%Y-%m-%dT%H:%M:%S", gmtime())))
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [stdout_handler, file_handler]

logging.basicConfig(level=logging.INFO, format=' %(levelname)s - %(message)s', handlers=handlers)
#[%(asctime)s] {%(filename)s:%(lineno)d}
logger = logging.getLogger()

class observation(object):
    _mjdref_ = 0
    _times_ = [0]
    _dtimes_ = [0]

    _gti_start_ = [0]
    _gti_stop_ = [0]
    _timezero_ = 0


class light_curve(observation):

    def __init__(self, nbins=1):
        self._times_ = np.zeros(nbins)
        self._dtimes_ = np.zeros(nbins)
        self._rates_ = np.zeros(nbins)
        self._drates_ = np.zeros(nbins)
        self._frac_exp_ = np.zeros(nbins)
        self._energy_ranges_ = [0]

        # self.read_from_fits(filename)

    def read_from_fits(self, filename):

        self._filename_ = filename
        ff = pf.open(filename)

        data_ind = 1
        gti_ind = 2

        self._times_ = ff[data_ind].data['TIME']
        self._rates_ = ff[data_ind].data['RATE']
        self._drates_ = ff[data_ind].data['ERROR']
        try:
            self._frac_exp_ = ff[data_ind].data['FRACEXP']
        except:
            logger.warning("Not found FRACEXP, defaulting to one")
            self._frac_exp_=np.ones(len(self._rates_))

        self._data_header_ = ff[data_ind].header
        try:
            self._gti_header_ = ff[gti_ind].header
        except:
            logger.warning("Not found GTI, ignoring")
            self._gti_header_ = None

        self._timeref_ = ff[data_ind].header['TIMEREF']
        self._timesys_ = ff[data_ind].header['TIMESYS']
        try:
            self._mjdref_ = ff[data_ind].header['MJDREF']
        except:
            logger.debug("Try to use MJDREFI and MJDREFF")
            self._mjdref_ = ff[data_ind].header['MJDREFI'] + ff[data_ind].header['MJDREFF']

        try:
            self._exposure_ = ff[data_ind].header['EXPOSURE']
        except:
            logger.warning("No Exposure")
            self._exposure_ = -1

        #TODO Use this value
        try:
            self._timepixr_ = ff[data_ind].header['TIMEPIXR']
        except:
            logger.warning('Not found TIMEPIXR, defaulting to zero')
            self._timepixr_ = 0

        self._timedel_ = ff[data_ind].header['TIMEDEL']

        self._tstart_ = ff[data_ind].header['TSTART']
        self._tstop_ = ff[data_ind].header['TSTOP']

        try:
            self._energy_ranges_ = [ff[data_ind].header['CHANMIN'], ff[data_ind].header['CHANMAX']]
        except:
            logger.info("Energy ranges not available")

        try:
            self._timezero_ = ff[data_ind].header['TIMEZERO']
        except:
            logger.info("TIMEZERO not available")

        try:
            self._dtimes_ = ff[data_ind].data['XAX_E']
        except:
            logger.info("Initializing delta_times from TIMEDEL")
            self._dtimes_ = np.ones(len(self._times_)) * self._timedel_

        if self._gti_header_ is not None:
            self._gti_start_ = self._gti_header_.data['START']
            self._gti_stop_ = self._gti_header_.data['STOP']
        else:
            logger.warning('No GTI, using data start and stop')
            self._gti_start_ = np.array([self._tstart_])
            self._gti_stop_ = np.array([self._tstop_])

        ff.close()
        self.dump_info()

    def dump_info(self):
        logger.info("The light curve %s has %d bin"%(self._filename_, len(self._times_)))
        logger.info("The light curve %s has %d GTI bin" % (self._filename_, len(self._gti_start_)))

    def from_lc(self, other):
        self._times_ = other._times_
        self._dtimes_ = other._dtimes_
        self._rates_ = other._rates_
        self._drates_ = other._drates_
        self._frac_exp_ = other._frac_exp_

        self._timeref_ = other._timeref_
        self._timesys_ = other._timesys_
        self._mjdref_ = other._mjdref_
        self._exposure_ = other._exposure_

        self._timedel_ = other._timedel_
        self._timezero_ = other._timezero_

        self._tstart_ = other._tstart_
        self._tstop_ = other._tstop_

        self._energy_ranges_ = other._energy_ranges_

        self._gti_start_ = other._gti_start_
        self._gti_stop_ = other._gti_stop_

        self._data_header_ = other._data_header_
        self._gti_header_ = other._gti_header_

    def __truediv__(self, other):

        if len(self._rates_) != len(other._rates_):
            raise RuntimeError('Light curves have different length')

        result = light_curve()
        result.from_lc(self)

        result._rates_ = self._rates_ / other._rates_
        tmp1 = (self._drates_ / self._rates_) ** 2
        tmp2 = (other._drates_ / other._rates_) ** 2

        result._drates_ = result._rates_ * np.sqrt(np.nan_to_num(tmp1, posinf=0, neginf=0) +
                                                   np.nan_to_num(tmp2, posinf=0, neginf=0))


        return result

    def __add__(self, other):

        if len(self._rates_) != len(other._rates_):
            raise RuntimeError('Light curves have different length')

        result = light_curve()
        result.from_lc(self)

        result._rates_ = self._rates_ + other._rates_
        result._drates_ = np.sqrt((self._drates_) ** 2 + (other._drates_) ** 2)

        return result

    def make_rebin_table(self, min_sn, max_time, gti_threshold, min_bin_size, max_point_sn, single_point_check):
        logger.debug("Making a rebin table for min S/N %f" % min_sn )
        logger.debug("Making a rebin table with GTI threshold %f" % gti_threshold)

        table = np.zeros(len(self._times_))
        tt = 0
        rr = 0
        ee = 0
        curr_gti_ind = 0
        gti_flag = 0
        end_flag = 0
        # // OUTPUT
        # // -2 discard for GTI
        # // -1 continue accumulation
        # // 0 discard
        # // 1 stop accumulation

        #
        # convenience variables
        #
        _x = self._times_
        _dx = self._dtimes_
        _y = self._rates_
        _dy = self._drates_

        logger.debug("The light curve size %d %d %d %d" % (len(_x), len(_dx), len(_y), len(_dy) ))

        n_gti = len(self._gti_start_)
        _size = len(self._times_)

        GTI_START = self._gti_start_ - self._timezero_
        GTI_STOP = self._gti_stop_ - self._timezero_

        tot_disregard_time = 0
        for i in range(_size):
            if i == _size - 1:
                end_flag = 1

            if (not np.isfinite(_y[i])) or (not np.isfinite(_dy[i])):
                continue

            if _y[i] != 0:
                if np.abs(_dy[i] / _y[i]) > max_point_sn:
                    logger.info("Point " + str(i) + " exceeds max_point_sn, discarded\n")
                    continue

            if n_gti > 1:
                if _x[i] < GTI_START[0] or _x[i] > GTI_STOP[n_gti - 1]:
                    logger.debug("Event %d out of GTI" % i)
                    table[i] = -2
                    continue

                if not (_x[i] >= GTI_START[curr_gti_ind] and _x[i] <= GTI_STOP[curr_gti_ind]):
                    logger.debug("Event # %d time %g not in gti bin %d %g -- %g " % (
                    i, _x[i], curr_gti_ind, GTI_START[curr_gti_ind],
                    GTI_STOP[curr_gti_ind]))

                    # Trivial checks to see if events are  out  of  GTI(it should not happen))
                    if curr_gti_ind > 0:

                        if _x[i] > GTI_STOP[curr_gti_ind - 1] and _x[i] < GTI_START[curr_gti_ind]:
                            table[i] = -2
                            continue

                    if curr_gti_ind < n_gti - 1:

                        if _x[i] < GTI_START[curr_gti_ind + 1] and _x[i] > GTI_STOP[curr_gti_ind]:
                            table[i] = -2
                            continue

                    # Check if we can continue accumulation despite the GTI break
                    # char neglect_gti=0;
                    # gti_flag=1 means stopping accumulation, gti_flag=0 means do not be bothered by the GTI
                    # to be checked
                    # removed < GTI_START[curr_gti_ind]
                    # Rememeber that we are outside the current GTI, so we have gone to the next one
                    if _x[i] - GTI_STOP[curr_gti_ind] <= gti_threshold:
                        logger.debug("Event does not exceed the GTI gap\n")
                        gti_flag = 0
                    else:
                        logger.debug("GTI Threshold exceeded Stop accumulation\n")
                        gti_flag = 1

                    # Increases GTI index
                    curr_gti_ind += 1
                    if (curr_gti_ind >= n_gti):
                        end_flag = 1
                        curr_gti_ind = n_gti - 1
            else:
                # In case no GTI is present
                delta_t = 0
                if i > 0:
                    delta_t = _x[i] - _x[i - 1]

                if delta_t >= gti_threshold:
                    logger.debug("Single GTI case, GTI threshold exceeded\n")
                    gti_flag = 1
                else:
                    gti_flag = 0

            if gti_flag > 0:
                logger.debug("Entered check for break in GTI exceeded!!")
                logger.debug("If not enough S/R, disregard all previous bins!!")

                if i == 0:
                    continue

                if rr <= min_sn * np.sqrt(ee):  # includes the rr=ee=0 case

                    local_t = 0

                    # remove points if not enough S / N is reached
                    for j in range(i - 1, 0, -1):  # (int j=i-1;j >= 0;j--)

                        # // cout << j << " " << table[j] << endl;
                        if (table[j] > 0):  # // | | _x[j] < GTI_START[curr_gti_ind-1] )
                            break
                        if (table[j] != -2):
                            local_t += _dx[j]

                        # // cerr << j << " = " << table[j] << " " << local_t << endl;

                        table[j] = 0

                    if (not end_flag):

                        if (n_gti > 0):
                            logger.debug(
                                "Disregard points in GTI bin interval #" + str(curr_gti_ind - 1) + " = [s]  " + str(
                                    100 * local_t / (
                                            GTI_STOP[curr_gti_ind - 1] - GTI_START[curr_gti_ind - 1])))
                        elif local_t > 0:
                            logger.debug("Disregard " + str(local_t) + " s for long gap at " + str(_x[i]))

                        tot_disregard_time += local_t
                        if (local_t < 0):
                            logger.error(" Negative local_t, stop\n")
                else:
                    # S/N is not reached
                    table[i - 1] = 1
                    # // cout << i << " " << rr / sqrt(ee) << " " << tt << " " << table[i] << endl;

                rr = 0
                ee = 0
                tt = 0
                gti_flag = 0
            # end of look in GTI FLAG
            if (single_point_check and (_y[i] / _dy[i]) >= min_sn):

                # // cout << "Point " << i << " has high S/N using it\n";

                table[i] = 1
                # // remove
                # points if not enough
                # S / N is reached \
                # "Removing points\n";

                local_t = 0

                for j in range(i - 1, 0, -1):  # (int j=i-1;j >= 0;j--):

                    # // cout << j << " " << table[j] << endl;
                    if (table[j] > 0):  # // | | _x[j] < GTI_START[curr_gti_ind-1] )
                        break

                    if (table[j] != -2):
                        local_t += _dx[j]

                        # // cerr << j << " = " << table[j] << " " << local_t << endl;

                        table[j] = 0
                    # End of discard loop

                tot_disregard_time += local_t
                if (local_t > 0):
                    logger.info(
                        "Disregard " + str(local_t) + " time units because I found a point with high S/N at index " + str(
                            i))

                if (local_t < 0):
                    logger.error(" Negative local_t, stop\n")

                rr = 0
                ee = 0
                tt = 0
                gti_flag = 0
                continue

            rr += _y[i]
            ee += (_dy[i]) ** 2

            # For data with large gaps. We use the time span not the bin size
            # In principle, should be cought by the GTI, INTEGRAL light curves in ASCII format
            # have not GTIs, produced manually from science window lists.
            # We should remove self patch and have proper GTIs for all light curves
            # The first condition tried to catch self

            if n_gti > 1:
                tt += _dx[i]
            else:
                if i == 0:
                    tt += _dx[i]
                else:
                    tt += (_x[i] + _dx[i] - _x[i - 1] - _dx[i - 1])

            # default value continue accumulation
            table[i] = -1

            if ee > 0:  # to avoid div by zero
                if (rr / np.sqrt(ee) >= min_sn and tt > min_bin_size) or tt >= max_time:
                    logger.debug("Entered loop check %d" % i)

                    if rr / np.sqrt(ee) < min_sn:
                        logger.debug("Removing points\n")
                        local_t = 0
                        # remove points if not enough S/N is reached
                        for j in range(i - 1, 0, -1):  # (int j=i;j >= 0;j--):
                            logger.debug("%d %d" % (j, table[j]))
                            if table[j] > 0:  # or _x[j] < GTI_START[curr_gti_ind-1] :
                                break
                            if table[j] != -2:
                                local_t += _dx[j]

                            logger.debug("%d = %d %f" %(j, table[j], local_t))

                            table[j] = 0

                        if not end_flag:
                            logger.debug("Not end flag")
                            if local_t < 0:
                                logger.error(" Negative local_t, stop\n")

                            tot_disregard_time += local_t

                            logger.info("Disregard points at index " + str(i) + " for " + str(local_t) +
                                        " time units due to maximum bin length or maximum time gap\n")
                    else:
                        logger.debug("Setting bin=1 at %d " % i )
                        table[i] = 1

                    logger.debug("%d %f %f %d" % (i, rr/np.sqrt(ee), tt, table[i]))
                    # waitkey()

                    rr = 0
                    ee = 0
                    tt = 0
                    gti_flag = 0
            elif gti_flag == 1:
                # cout << "GTI FLAG\n"
                local_t = 0

                for j in range(i - 1, 0, -1):  # (int j=i;j >= 0;j--)
                    if table[j] == 1:  # or _x[j] < GTI_START[curr_gti_ind-1] :
                        break
                    if table[j] != -2:
                        local_t += _dx[j]

                    table[j] = 0
                # cout << j  << " GF= " << _dx[j] << " " << local_t << endl

                if not end_flag:
                    logger.debug("gti_flag, disregard points in interval " + str(curr_gti_ind - 1) + " = [s]  " +
                                str(100 * local_t / (GTI_STOP[curr_gti_ind - 1] - GTI_START[
                                    curr_gti_ind - 1])) )

                    if local_t < 0:
                        logger.error(" Negative local_t, stop\n")

                    tot_disregard_time += local_t

                gti_flag = 0

        logger.info("Total disregarded time is [s] " + str(tot_disregard_time))



        return table

    def rebin(self, table):

        new_x = []
        new_dx = []
        new_y = []
        new_dy = []
        new_frac_exp = []

        nx = 0
        ndx = 0
        ny = 0
        ndy = 0
        nn = 0
        nf = 0
        tmin = 1e100
        tmax = -1e100

        # ofstream ff("rebin_table.txt")
        # for(int i=0;i<_size;i++)
        #     ff << i << " " << table[i] << endl
        # ff.close()

        # -2 discard for GTI
        # -1 continue accumulation
        # 0 discard
        # 1 stop accumulation

        # ofstream out_tmp("try.txt")
        _size = len(self._times_)
        _x = self._times_
        _dx = self._dtimes_
        _y = self._rates_
        _dy = self._drates_

        for i in range(_size):

            # out_tmp << i << " " << _x[i] << " " << table[i] << endl
            if (not np.isfinite(_y[i])) or (not np.isfinite(_dy[i])):
                continue

            if table[i] != 0 and table[i] != -2:
                nx += _x[i] + _dx[i] / 2  # we have assumed _x as initial time of the bin
                ndx += _dx[i]
                ny += _y[i] * _dx[i]
                ndy += (_dy[i]*_dx[i]) ** 2
                nf += self._frac_exp_[i] * _dx[i]
                #			if _frac_exp[i]:
                #				nn_nonnull++
                if tmin > _x[i]:
                    tmin = _x[i]

                if tmax < _x[i] + _dx[i]:
                    tmax = _x[i] + _dx[i]

                nn += 1
                if np.isnan(ny) or np.isnan(ndy):
                    logger.error("%d %f %f %f %f" % (i, _x[i], _dx[i], _y[i], _dy[i]))
                    logger.error("%d %f %f %f %f" % (i, nx, ndx, ny, ndy))
                    # break
                    nx = 0
                    ndx = 0
                    ny = 0
                    ndy = 0
                    nn = 0
                    nf = 0
                    tmin = 1e100
                    tmax = -1e100

            if table[i] == 1 or i == _size - 1:
                if i == _size - 1:
                    logger.debug("Arrived to the end\n")
                if nn > 0 and ndx > 0:
                    new_x.append(tmin)  # inital time of the bin
                    new_dx.append(tmax - tmin)

                    # test
                    # new_x.append(nx/nn-ndx/2)
                    # new_dx.append(ndx)

                    new_y.append(ny)
                    new_dy.append(np.sqrt(ndy))
                    new_frac_exp.append(nf / (tmax - tmin))
                    # cout << i << " " << nx/nn << " " << ndx << " " << ny/ndx << " " << sqrt(ndy)/ndx << " " << nn << endl
                    if ny == 0:
                        if i == _size - 1:
                            logger.warning("WARNING . The last bin has zero counts, should remove it by hand\n")
                        else:
                            logger.warning(
                                "WARNING . bin with zero counts in the middle of the curve: it should not happen\n")

                    nx = 0
                    ndx = 0
                    ny = 0
                    ndy = 0
                    nn = 0
                    nf = 0
                    tmin = 1e100
                    tmax = -1e100


                else:
                    logger.debug("No signal\n")

        if len(new_x) <= 1:
            logger.error("No suitable rebinning table")
            for i in range(_size):
                logger.debug("%d %d" % (i, table[i]))

            return 1

        logger.info("Rebinning, LC will have " +str(len(new_x)) + " bins")

        self._times_ = np.array(new_x)
        self._dtimes_ = np.array(new_dx)
        self._rates_ = np.array(new_y) / self._dtimes_
        self._drates_ = np.array(new_dy) / self._dtimes_
        self._frac_exp_ = new_frac_exp


def hratio_func(soft_lcname, hard_lcname, hratio_fname, min_sn: float, max_time=1e4, gti_threshold=100, flag_rebin=1, min_bin_size=0,
           ext_t0=-1, max_point_sn=100, single_point_check=False):

    logger.info("Soft LC " + soft_lcname)
    logger.info("Hard LC " + hard_lcname)

    if hratio_fname is not None:
        logger.info("Hardness ratio output file " + hratio_fname)
    else:
        logger.info("No Hardness ratio file")

    logger.info("Minimun S/N %f" % min_sn)
    logger.info("Maximum bin length %f" % max_time)
    logger.info("Threshod to use a GTI gap %f" % gti_threshold)
    flag_rebin_dict = {
        1: "soft",
        2: "Hard",
        3: "Summed",
        4: "Hardness ratio"
    }
    logger.info("Rebin on %s light curve" % flag_rebin_dict[flag_rebin])
    logger.info("Minimum bin size %f" % min_bin_size)
    logger.info("External T0 %f (if <0, first bin)" % ext_t0)
    logger.info("Check on single point %r" % single_point_check)
    logger.info("Maximum allowed S/N for one point %f\n\n" % max_point_sn)

    soft_lc = light_curve()
    soft_lc.read_from_fits(soft_lcname)
    hard_lc = light_curve()
    hard_lc.read_from_fits(hard_lcname)

    if flag_rebin == 1:
        table = soft_lc.make_rebin_table(min_sn, max_time, gti_threshold, min_bin_size, max_point_sn,
                                         single_point_check)
    elif flag_rebin == 2:
        table = hard_lc.make_rebin_table(min_sn, max_time, gti_threshold, min_bin_size, max_point_sn,
                                         single_point_check)
    elif flag_rebin == 3:
        sum_lc = soft_lc + hard_lc
        table = sum_lc.make_rebin_table(min_sn, max_time, gti_threshold, min_bin_size, max_point_sn,
                                        single_point_check)
    elif flag_rebin == 4:
        sum_lc = soft_lc / hard_lc
        table = sum_lc.make_rebin_table(min_sn, max_time, gti_threshold, min_bin_size, max_point_sn,
                                        single_point_check)
    else:
        raise RuntimeError("Unknown flag for rebin")

    soft_lc.rebin(table)
    hard_lc.rebin(table)

    hratio_lc = hard_lc / soft_lc

    if hratio_fname is not None:
        write_qdp(soft_lc, hard_lc, hratio_lc, hratio_fname, ext_t0)

    return soft_lc, hard_lc, hratio_lc


def write_qdp(soft_lc, hard_lc, hratio_lc, hratio_fname, ext_t0):
    ff = open(hratio_fname, 'w')
    ff.write("read serr 1 2 3 4\n")
    ff.write("cpd /xw\n")
    ff.write('scr white\n')
    # ff << "ma 1 on 2\n";
    ff.write("lw 2\n")
    ff.write("cs 1.1\n")
    ff.write("font roman\n")
    ff.write("time off\n")
    ff.write("lab title\n")

    off_time = 0
    scale_unit = 1
    if soft_lc._times_[0] > 1e8 and ext_t0 < 0:
        logger.debug("Use first bin as t0 : %f %f " % (soft_lc._times_[0], ext_t0))
        off_time = np.floor(soft_lc._times_[0])
        ff.write("lab x Time since %f\n" % (off_time / scale_unit))
        ff.write("!lab x Time since %s\n" % (off_time))
    elif ext_t0 >= 0:
        logger.debug("Use ext_t0 : %f " % (ext_t0))
        off_time = np.floor(ext_t0)
        ff.write("lab x Time since %f\n" % (off_time / scale_unit))
        ff.write("!lab x Time since %f\n" % off_time)
    else:
        logger.debug("Does not use a t0 : %f %f " % (soft_lc._times_[0], ext_t0))
        ff.write("lab x Time [s]\n")

    ff.write("lab y2 Soft [cts/s]\n")
    ff.write("lab y3 Hard [cts/s]\n")
    ff.write("lab y4 Hardness ratio\n")

    ff.write("r x %19.12e %19.12e\n" % ((soft_lc._times_[0] - off_time) / scale_unit,
                                        (soft_lc._times_[-1] + 2 * soft_lc._dtimes_[-1] - off_time) / scale_unit))

    ff.write("plot vert\n")

    for i in range(len(soft_lc._times_)):
        ff.write("%19.12e %19.12e %19.12e %19.12e %19.12e %19.12e %19.12e %19.12e\n" % (
            (soft_lc._times_[i] - off_time + soft_lc._dtimes_[i] / 2.0) / scale_unit,
            soft_lc._dtimes_[i] / 2.0 / scale_unit,
            soft_lc._rates_[i],
            soft_lc._drates_[i],
            hard_lc._rates_[i],
            hard_lc._drates_[i],
            hratio_lc._rates_[i],
            hratio_lc._drates_[i]))

    ff.close()

@click.command()
@click.argument("soft_lcname", nargs=1) #, help="The soft light curve in fits format"
@click.argument("hard_lcname", nargs=1) #, help="The soft light curve in fits format"
@click.argument("hratio_fname", nargs=1) #, help="The output hardness ratio (.qdp in qdp format)"
@click.argument("min_sn", nargs=1) #, help="The minimum S/N to rebin"
@click.option("--max_time", default=1e4,
              help="Maximum time interval. It does not accumulate longer bins, regardless of S/N and it removes all previous points.")
@click.option("--gti_threshold", default=100.,
              help="Threshold to use a GTI GAP. It discards all previous data if a gti gap is larger than this value and S/N threshold is not reached.")
@click.option("--flag_rebin", default=1, help="Use soft (1) hard (2), sum (3), or HR (4) for rebinning")
@click.option("--min_bin_size", default=0., help="Minimum time bin size. No shorter bins are allowed.")
@click.option("--ext_t0", default=-1.0, help="Input T0 in seconds (if <0 use first bin of data)")
@click.option("--max_point_sn", default=100., help="The maximum noise over signal ratio allowed (to avoid very noisy points)")
@click.option("--single_point_check/--no-single_point_check", default=False,
              help="Do you want to enable breaking of accumulation if a single point with S/N exceeding threshold is enountered?")
def hratio(soft_lcname, hard_lcname, hratio_fname, min_sn, max_time, gti_threshold, flag_rebin, min_bin_size,
           ext_t0, max_point_sn, single_point_check):

    """Makes the hardness ratio of two light curves after adaptive rebin.

    hratio soft_lcname  hard_lcname hratio_fname min_sn

    soft_lcname  STRING The soft light curve in fits format
    hard_lcname  STRING The soft light curve in fits format
    hratio_fname STRING The output hardness ratio (.qdp in qdp format)
    min_sn       FLOAT The minimum S/N to rebin
    """


    hratio_func(soft_lcname, hard_lcname, hratio_fname, float(min_sn), max_time, gti_threshold, flag_rebin,
                min_bin_size, ext_t0, max_point_sn, single_point_check)

if __name__ == "__main__":
    hratio()
