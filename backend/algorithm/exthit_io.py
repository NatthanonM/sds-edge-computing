class ExtHit_IO:
    def __init__(self, top_n, rssi, training_data: list, removed_access_points: list = []):
        self.top_n = top_n
        self.rssi = rssi
        self.universe_ap = set()
        self.raw_training_data = training_data.copy()
        self.raw_testing_data = []
        self.training_data = {}
        self.testing_data = []
        self.threshold = {}
        self.removed_access_points = removed_access_points.copy()
        self.train()

    def remove_detected_BSSID(self):
        for t in self.raw_training_data:
            size = len(t['access_point'])
            for i in range(size - 1, -1, -1):
                if t['access_point'][i]['BSSID'] in self.removed_access_points:
                    del t['access_point'][i]

    def calculate_threshold(self):
        for t in self.raw_training_data:
            if t['environment'] == 'indoor':
                s = self.get_valid_access_point(t['access_point'])
                fingerprint = self.training_data[t['building_id']]
                hit_score = self.calculate_hit_score(fingerprint, s)

                if ((t['building_id'] in self.threshold) and hit_score < self.threshold[t['building_id']]) \
                        or t['building_id'] not in self.threshold:
                    self.threshold[t['building_id']] = hit_score

    def create_fingerprint(self):
        for t in self.raw_training_data:
            if t['environment'] == 'indoor':
                if t['building_id'] not in self.training_data:
                    self.training_data[t['building_id']] = set()
                self.training_data[t['building_id']].update(
                    self.get_BSSID(t['access_point'][0:self.top_n]))

    def train(self):
        self.remove_detected_BSSID()
        self.create_fingerprint()
        self.calculate_threshold()

    def get_valid_access_point(self, access_point):
        temp_ap = access_point[0:self.top_n]
        ap = []
        for t in temp_ap:
            if t['RSSI'] >= self.rssi:
                ap.append(t['BSSID'])
        return ap

    def get_BSSID(self, access_point):
        bssid = []
        for ap in access_point:
            bssid.append(ap['BSSID'])
        return bssid

    def filter_unknown_BSSID(self):
        for f in self.raw_training_data:
            for ap in f['access_point']:
                self.universe_ap.add(ap['BSSID'])

        for s in self.raw_testing_data:
            size = len(s['access_point'])
            for i in range(size - 1, -1, -1):
                if s['access_point'][i]['BSSID'] not in self.universe_ap:
                    del s['access_point'][i]

    def calculate_hit_score(self, fingerprint, sampling):
        hit_score = 0
        for bssid in sampling:
            if bssid in fingerprint:
                hit_score += 1
        return hit_score

    def get_answer(self, hit_score):
        predicted_building_id = 'XXX'
        predicted_environment = 'outdoor'
        for building in hit_score:
            if hit_score[building] >= self.threshold[building]:
                predicted_building_id = building
                predicted_environment = 'indoor'
        return {'predicted_environment': predicted_environment, 'predicted_building_id': predicted_building_id}

    def predict_all(self, testing_data: list):
        self.raw_testing_data = testing_data.copy()
        self.filter_unknown_BSSID()

        for t in self.raw_testing_data:
            t['access_point'] = self.get_valid_access_point(t['access_point'])
            self.testing_data.append(t)

        predicted_result = []

        for sampling in self.testing_data:
            s = sampling['access_point']
            hit_score = {}
            for building in self.training_data:
                fingerprint = self.training_data[building]
                hit_score[building] = self.calculate_hit_score(fingerprint, s)

            answer = self.get_answer(hit_score)

            predicted_result.append(
                {'key_environment': sampling['environment'], 'key_building_id': sampling['building_id'],
                 'key_tag': sampling['tag'], 'key_floor': sampling['floor'],
                 'predicted_environment': answer['predicted_environment'],
                 'predicted_building_id': answer['predicted_building_id']})

        return predicted_result

    def localize(self, sampling):
        hit_score = {}
        for building in self.training_data:
            fingerprint = self.training_data[building]
            hit_score[building] = self.calculate_hit_score(
                fingerprint, self.get_valid_access_point(sampling))
        answer = self.get_answer(hit_score)
        return answer['predicted_environment']
