import qrunner


class TestApiSample(qrunner.TestCase):

    @qrunner.file_data('card_type', 'data.json')
    def test_case_01(self, card_type):
        path = '/api/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        pay_load = {"type": card_type}
        self.post(path, json=pay_load)
