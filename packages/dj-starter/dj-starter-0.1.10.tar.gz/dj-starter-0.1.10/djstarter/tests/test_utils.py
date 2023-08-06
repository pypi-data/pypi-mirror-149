from datetime import datetime, timezone

from django.test import TestCase, TransactionTestCase

from djstarter import utils


class QueuedExecutorTests(TransactionTestCase):
    def test_queued_thread_executor(self):
        def double(x): return 2 * x

        with utils.QueuedThreadExecutor(max_workers=5) as executor:

            future = executor.submit(double, 8)
            self.assertEquals(future.result(), 16)

            def raise_error(): raise ValueError
            future = executor.submit(raise_error)
            with self.assertRaises(ValueError):
                future.result()

        with self.assertRaises(RuntimeError):
            executor.submit(double, 8)


class BoundedExecutorTests(TransactionTestCase):
    def test_bounded_thread_executor(self):
        def double(x): return 2 * x

        with utils.BoundedThreadExecutor(max_workers=1) as executor:

            future = executor.submit(double, 8)
            self.assertEquals(future.result(), 16)

            def raise_error(): raise ValueError
            future = executor.submit(raise_error)
            with self.assertRaises(ValueError):
                future.result()

        with self.assertRaises(RuntimeError):
            executor.submit(double, 8)


class PagerTests(TestCase):
    def test_pager_invalid_items_count(self):
        with self.assertRaises(ValueError):
            utils.Pager(items_count=0)

        with self.assertRaises(ValueError):
            utils.Pager(items_count=-333)

    def test_pager_page_number_less_than_1(self):
        pager = utils.Pager(items_count=999, items_per_page=111)

        with self.assertRaises(ValueError):
            pager.items_on_page(0)

        with self.assertRaises(ValueError):
            pager.items_on_page(-23)

    def test_pager_page_number_exceeds_last_page(self):
        pager = utils.Pager(items_count=999, items_per_page=111)

        with self.assertRaises(ValueError):
            pager.items_on_page(10)

        pager = utils.Pager(items_count=1525, items_per_page=25)

        with self.assertRaises(ValueError):
            pager.items_on_page(62)

    def test_pager_offset(self):
        pager = utils.Pager(items_count=1, items_per_page=1)

        self.assertEquals(pager.offset(1), 0)
        self.assertEquals(pager.offset(pager.last_page_number), 0)

        pager = utils.Pager(items_count=999, items_per_page=111)

        self.assertEquals(pager.offset(4), 333)
        self.assertEquals(pager.offset(7), 666)
        self.assertEquals(pager.offset(pager.last_page_number), 888)

        pager = utils.Pager(items_count=1525, items_per_page=23)

        self.assertEquals(pager.offset(4), 69)
        self.assertEquals(pager.offset(7), 138)
        self.assertEquals(pager.offset(pager.last_page_number), 1518)

    def test_pager_last_page_number(self):
        pager = utils.Pager(items_count=1, items_per_page=1)

        self.assertEquals(pager.last_page_number, 1)

        pager = utils.Pager(items_count=999, items_per_page=111)

        self.assertEquals(pager.last_page_number, 9)

        pager = utils.Pager(items_count=1525, items_per_page=23)

        self.assertEquals(pager.last_page_number, 67)

    def test_pager_last_page_items_count(self):
        pager = utils.Pager(items_count=1, items_per_page=1)

        self.assertEquals(pager.last_page_items_count, 1)

        pager = utils.Pager(items_count=999, items_per_page=111)

        self.assertEquals(pager.last_page_items_count, 111)

        pager = utils.Pager(items_count=1525, items_per_page=23)

        self.assertEquals(pager.last_page_items_count, 7)

    def test_pager_items_on_page(self):
        pager = utils.Pager(items_count=1, items_per_page=1)

        self.assertEquals(pager.items_on_page(1), 1)
        self.assertEquals(pager.items_on_page(pager.last_page_number), 1)

        pager = utils.Pager(items_count=999, items_per_page=111)

        self.assertEquals(pager.items_on_page(2), 111)
        self.assertEquals(pager.items_on_page(7), 111)
        self.assertEquals(pager.items_on_page(pager.last_page_number), 111)

        pager = utils.Pager(items_count=1525, items_per_page=23)

        self.assertEquals(pager.items_on_page(3), 23)
        self.assertEquals(pager.items_on_page(11), 23)
        self.assertEquals(pager.items_on_page(pager.last_page_number), 7)


class UtilTests(TestCase):
    """
    Utility Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.test_str = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'

    def test_choice_enum(self):
        class Statuses(utils.ChoiceEnum):
            INIT = 0
            RUNNING = 1
            ERROR = 2

        self.assertListEqual(Statuses.choices(), [(0, 'INIT'), (1, 'RUNNING'), (2, 'ERROR')])
        self.assertListEqual(Statuses.labels(), ['INIT', 'RUNNING', 'ERROR'])
        self.assertEquals(Statuses.by_label('RUNNING'), 1)

    def test_abbrev_str(self):
        self.assertEquals(utils.abbrev_str(self.test_str, max_length=10), 'Lorem ipsu...')
        self.assertEquals(utils.abbrev_str(self.test_str, max_length=100), self.test_str)

    def test_eye_catcher_line(self):
        self.assertEquals(utils.eye_catcher_line(self.test_str), f'####  {self.test_str}  ####')

    def test_get_weighted_item(self):
        items = [('abc', .25), ('def', .25), ('jkl', .5)]
        item = utils.get_weighted_item(items)
        self.assertIsNotNone(item)

    def test_obj_to_json(self):
        class Main1:
            class Sub1:
                def __init__(self, test_1):
                    self.test_1 = test_1

            def __init__(self, arg_1, arg_2, arg_3):
                self.arg_1 = arg_1
                self.arg_2 = arg_2
                self.arg_3 = self.Sub1(arg_3)

        obj = Main1(arg_1='value_1', arg_2='value_2', arg_3='value_3')
        self.assertEquals(
            utils.obj_to_json(obj),
            '{"arg_1":"value_1","arg_2":"value_2","arg_3":{"test_1":"value_3"}}'
        )

    def test_pretty_dict(self):
        obj = {
            't_1': 'val_1',
            't_8': {
                'l_3': 'val_3',
            },
            'test_7': {
                'l_19': 'val_30',
                'l_12': 'val_17'
            },
        }
        self.assertEquals(
            utils.pretty_dict(obj),
            ("{\n    \"t_1\": \"val_1\",\n    \"t_8\": {\n        \"l_3\": \"val_3\"\n    },\n    \"test_7\": {\n"
             "        \"l_12\": \"val_17\",\n        \"l_19\": \"val_30\"\n    }\n}")
        )

    def test_past_unix_timestamp_ss(self):
        start = 1635483705

        timestamp = utils.past_unix_timestamp_ss(unix_timestamp=start, hours=6)
        self.assertIsInstance(timestamp, int)
        self.assertEquals(timestamp, 1635462105)

        timestamp = utils.past_unix_timestamp_ss(unix_timestamp=start, days=2)
        self.assertEquals(timestamp, 1635310905)

        timestamp = utils.past_unix_timestamp_ss(unix_timestamp=start, days=7)
        self.assertEquals(timestamp, 1634878905)

        timestamp = utils.past_unix_timestamp_ss(unix_timestamp=start, days=28)
        self.assertEquals(timestamp, 1633064505)

        timestamp = utils.past_unix_timestamp_ss(unix_timestamp=start, days=1826)   # 5 years
        self.assertEquals(timestamp, 1477717305)

    def test_url_file_ext(self):
        test_url_1 = ('https://external-preview.redd.it/mPeN_GXOIAZmu1qO_gpQNiItIqiqbPL-Np_Hncp7_Mg.png?format=pjpg'
                      '&auto=webp&s=d51a4b61d82bcb2415de35e1ef35d986d2aad8d6')
        self.assertEquals(utils.get_file_ext(test_url_1), '.png')

        test_url_2 = 'https://imgur.com/V6lKWen.jpg'
        self.assertEquals(utils.get_file_ext(test_url_2), '.jpg')

    def test_get_path(self):
        test_url_1 = ('https://external-preview.redd.it/mPeN_GXOIAZmu1qO_gpQNiItIqiqbPL-Np_Hncp7_Mg.png?format=pjpg'
                      '&auto=webp&s=d51a4b61d82bcb2415de35e1ef35d986d2aad8d6')
        self.assertEquals(utils.get_path(test_url_1), '/mPeN_GXOIAZmu1qO_gpQNiItIqiqbPL-Np_Hncp7_Mg.png')

        test_url_2 = 'https://imgur.com/V6lKWen.jpg'
        self.assertEquals(utils.get_path(test_url_2), '/V6lKWen.jpg')

    def test_get_mimetype(self):
        test_url_1 = ('https://external-preview.redd.it/mPeN_GXOIAZmu1qO_gpQNiItIqiqbPL-Np_Hncp7_Mg.png?format=pjpg'
                      '&auto=webp&s=d51a4b61d82bcb2415de35e1ef35d986d2aad8d6')
        self.assertEquals(utils.get_mimetype(test_url_1), 'image/png')

        test_url_2 = 'https://imgur.com/V6lKWen.jpg'
        self.assertEquals(utils.get_mimetype(test_url_2), 'image/jpeg')

    def test_utf_16_decode(self):
        test_msg = '\ud83d\udd25 Whale swimming casually among a group of surfers unaware of his presence.'

        val = utils.utf_16_decode(test_msg)
        self.assertEquals(val, '🔥 Whale swimming casually among a group of surfers unaware of his presence.')

        test_msg = '\u201cAlright, is it going to be a Palkia?\u201d'
        val = utils.utf_16_decode(test_msg)

        self.assertEquals(val, '“Alright, is it going to be a Palkia?”')

    def test_exponential_decay(self):
        hours = 18
        seconds = hours * 60 * 60

        init_y = 1.0
        lower_bound = .23
        tau = 20000

        val = utils.exponential_decay(t=0, y_init=init_y, tau=tau, y_min=lower_bound)
        self.assertEquals(val, 1.0)

        val = utils.exponential_decay(t=1000, y_init=init_y, tau=tau, y_min=lower_bound)
        self.assertAlmostEquals(val, 0.9624466568655498, places=8)

        val = utils.exponential_decay(t=2000, y_init=init_y, tau=tau, y_min=lower_bound)
        self.assertAlmostEquals(val, 0.9267248118876888, places=8)

        val = utils.exponential_decay(t=10000, y_init=init_y, tau=tau, y_min=lower_bound)
        self.assertAlmostEquals(val, 0.6970286079787278, places=8)

        val = utils.exponential_decay(t=50000, y_init=init_y, tau=tau, y_min=lower_bound)
        self.assertAlmostEquals(val, 0.29320544894040207, places=8)

        val = utils.exponential_decay(t=seconds, y_init=init_y, tau=tau, y_min=lower_bound)
        self.assertAlmostEquals(val, 0.2601561992262201, places=8)

    def test_iso8601_timestamp_to_unix(self):
        self.assertEquals(utils.iso8601_timestamp_to_unix(''), '')
        self.assertEquals(utils.iso8601_timestamp_to_unix('2021-12-24T22:00:49.000Z'), 1640383249)
        self.assertEquals(utils.iso8601_timestamp_to_unix('2021-12-23T07:25:56.000Z'), 1640244356)

    def test_iso8601_timestamp_to_datetime(self):
        self.assertEquals(utils.iso8601_timestamp_to_datetime(''), '')

        dt = utils.iso8601_timestamp_to_datetime('2021-12-24T22:00:49.000Z')
        self.assertEquals(dt, datetime(2021, 12, 24, 22, 00, 49, tzinfo=timezone.utc))

        dt = utils.iso8601_timestamp_to_datetime('2021-12-23T07:25:56.000Z')
        self.assertEquals(dt, datetime(2021, 12, 23, 7, 25, 56, tzinfo=timezone.utc))

    def test_add_jitter(self):
        self.assertTrue(.5 <= utils.add_jitter(min_value=0, jitter=.5, val=1.0) <= 1.5)
        self.assertTrue(11 <= utils.add_jitter(min_value=11, jitter=20, val=15.5) <= 35.5)
        self.assertTrue(0.1437 <= utils.add_jitter(min_value=.07, jitter=.0123, val=.156) <= 0.1683)

    def test_dice_roll(self):
        is_true = utils.dice_roll(chance=1)
        self.assertTrue(is_true)

        is_false = utils.dice_roll(chance=0)
        self.assertFalse(is_false)

        with self.assertRaises(ValueError):
            utils.dice_roll(chance=2.05)

        with self.assertRaises(ValueError):
            utils.dice_roll(chance=-.09)
