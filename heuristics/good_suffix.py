from heuristics.heuristics import Heuristic


class GoodSuffix(Heuristic):
    def _set_occ_dict(self, occ_dict):
        self._occ_dict=occ_dict

    def _get_occ_dict(self):
        return self._occ_dict

    def _set_shift_array(self, shift_array):
        self._shift_array=shift_array

    def _get_shift_array(self):
        return self._shift_array

    def preprocess_first_case(pattern_, shift_array, bpos):
        m=len(pattern_)
        i=m
        j=m + 1
        bpos[i]=j
        while i > 0:
            while (j <= m and pattern_[i - 1] != pattern_[j - 1]):
                if shift_array[j] == 0:
                    shift_array[j]=j - i
                j=bpos[j]
            i-=1
            j-=1
            bpos[i]=j

    def create_occ_dict(pattern_):
        occ_dict={}
        for i in range(len(pattern_)):
            occ_dict[pattern_[i]]=i
        return occ_dict

    def preprocess_second_case(pattern_, shift_array, bpos):
        j=bpos[0]
        m=len(pattern_)
        for i in range(m + 1):
            if shift_array[i] == 0:
                shift_array[i]=j
            if i == j:
                j=bpos[j]

    def preprocess(self, pattern_, alphabet=None):
        self._set_occ_dict(GoodSuffix.create_occ_dict(pattern_))
        m=len(pattern_)
        bpos_temp=[0] * (m + 1)
        shift_array_temp=[0] * (m + 1)
        GoodSuffix.preprocess_first_case(pattern_, shift_array_temp, bpos_temp)
        GoodSuffix.preprocess_second_case(pattern_, shift_array_temp, bpos_temp)
        self._set_shift_array(shift_array_temp)

    def get_offset_matched(self, **kwargs):
        return self._get_shift_array()[0]

    def get_offset_mismatched(self, **kwargs):
        cur_letter=kwargs['cur_letter']
        index=kwargs['mismatch_offset']
        return max(self._get_shift_array()[index + 1], index - self._get_occ_dict().get(cur_letter, -1))

    def get_name(self):
        return "Good suffix"
