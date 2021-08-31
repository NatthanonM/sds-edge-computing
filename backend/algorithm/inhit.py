from operator import itemgetter


class InHit:
    def __init__(self, top_n, rssi_diff, top_fingerprint, training_data: list, missing_access_points: list = []):
        self.top_n = top_n
        self.rssi_diff = rssi_diff
        self.raw_training_data = training_data.copy()
        self.training_data = []
        self.testing_data = []
        self.top_fingerprint = top_fingerprint
        self.missing_access_points = missing_access_points.copy()
        self.train()

    def remove_detected_BSSID(self):
        for t in self.training_data:
            size = len(t['access_point'])
            for i in range(size - 1, -1, -1):
                if t['access_point'][i]['BSSID'] in self.missing_access_points:
                    del t['access_point'][i]

    def create_fingerprint(self):
        for t in self.raw_training_data:
            if t['environment'] == 'indoor':
                sc = t.copy()
                sc['access_point'] = t['access_point'][0:self.top_n]
                self.training_data.append(sc)

    def train(self):
        self.remove_detected_BSSID()
        self.create_fingerprint()

    def predict_all(self, testing_data: list):
        self.testing_data = testing_data.copy()

        for t in self.testing_data:
            t['access_point'] = t['access_point'][0:self.top_n]
        match = 0
        not_match = 0
        predicted_result = []
        not_match_list = []
        for sampling in self.testing_data:
            s = sampling['access_point']
            for fingerprint in self.training_data:
                f = fingerprint['access_point']
                fingerprint['hit_score'] = self.calculate_hit_score(f, s)
            answer = self.get_answer()
            predicted_result.append(
                {'match': sampling['floor'] == answer['floor'] and sampling['tag'] == answer['tag'], 'key_floor': sampling['floor'], 'key_tag': sampling['tag'], 'predicted_location': answer})
            if sampling['floor'] == answer['floor'] and sampling['tag'] == answer['tag']:
                match += 1
            else:
                not_match += 1
                not_match_list.append(
                    {'key_floor': sampling['floor'], 'key_tag': sampling['tag'], 'predicted_location': answer})
        return predicted_result

    def calculate_hit_score(self, f, s):
        hit_score = 0
        for ap_s in s:
            for ap_f in f:
                if ap_s['BSSID'] == ap_f['BSSID']:
                    if abs(ap_s['RSSI'] - ap_f['RSSI']) <= self.rssi_diff:
                        hit_score += 1
                    break
        return hit_score

    def get_answer(self):
        hit_score = []
        for f in self.training_data:
            hit_score.append(
                {'hit_score': f['hit_score'], 'floor': f['floor'], 'tag': f['tag']})

        sorted_list = sorted(
            hit_score, key=itemgetter('hit_score'), reverse=True)
        most_match_fingerprint = sorted_list[0:self.top_fingerprint]
        # sum_hit_score = 0
        # sum_tag = 0
        # for fp in most_match_fingerprint:
        #     sum_hit_score += fp['hit_score']
        #     sum_tag += (fp['tag'] * fp['hit_score'])
        # final_tag = (sum_tag + 0.0) / sum_hit_score

        location = {
            'floor': most_match_fingerprint[0]['floor'], 'tag': most_match_fingerprint[0]['tag']}

        return location

    def localize(self, sampling: list):
        for fingerprint in self.training_data:
            f = fingerprint['access_point']
            fingerprint['hit_score'] = self.calculate_hit_score(
                f, sampling[0:self.top_n])
        answer = self.get_answer()
        return answer
