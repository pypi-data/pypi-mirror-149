# from weightsplitter.main import WeightSplitter
import threading

from ws_one_stable.main import WeightSplitter
from traceback import format_exc
from wsqluse.wsqluse import Wsqluse
from hermessplitter import functions
from hermessplitter.db import db_funcs
from hermessplitter.fast_api import main
import multiprocessing


class HermesSplitter(WeightSplitter):
    def __init__(self, ip, port,
                 wdb_name, wdb_user, wdb_pass, wdb_host,
                 port_name='/dev/ttyUSB0', terminal_name='CAS',
                 debug=False):
        #multiprocessing.Process(target=main.run_uvicorn, args=()).start()
        super().__init__(ip, port, debug=debug, port_name=port_name,
                         terminal_name=terminal_name)
        self.notes = ''
        self.active = False
        #threading.Thread(target=self.start_fast_api, args=()).start()
        self.kf = 0
        self.hermes_weight = 0
        self.avg_tara = 0
        self.max_brutto = 0
        self.avg_weight = 0
        self.test_mode = self.define_if_test_mode()
        self.wdb_sqlshell = Wsqluse(wdb_name, wdb_user, wdb_pass, wdb_host)
        self.ar = None # not realized
        threading.Thread(target=functions.import_clients, args=(self.wdb_sqlshell,)).start()
        threading.Thread(target=main.run_uvicorn, args=()).start()

    def start_fast_api(self):
        main.run_uvicorn()

    def define_if_test_mode(self):
        result = db_funcs.get_test_mode()
        result_frmt = int(result[0])
        if result_frmt:
            return True

    def tracing_thread(self):
        while True:
            if not self.ar.status_ready:
                self.activate(carnum=self.ar.round_status_dict['car_number'],
                              client=self.ar.round_status_ready['carrier'])
                while True:
                    pass

    def activate(self, carnum, record_id, client=None):
        """ Активировать HERMES """
        if functions.check_hermes_active():
            self.record_id = record_id
            # kf = functions.get_kf(self.wdb_sqlshell, carrier=client)
            kf = db_funcs.get_client_kf_by_ex_id(client)
            try:
                if kf:
                    kf = kf[0] * 0.01
                else:
                    return
            except: return
            print('Получен KF Hermes =', kf)
            avg_tara = functions.get_avg_tara(self.wdb_sqlshell, carnum)
            max_brutto = functions.get_max_weight(self.wdb_sqlshell, carnum)
            avg_weigth = functions.get_avg_weight(self.wdb_sqlshell, carnum)
            self.notes = ''
            self.set_kf(kf)
            self.set_status(True)
            self.set_debug(self.debug)
            self.set_avg_tara(avg_tara)
            self.set_max_brutto(max_brutto)
            self.set_avg_weigth(avg_weigth)

    def set_kf(self, kf):
        self.show_print('setting kf', kf, debug=True)
        self.kf = 1.0 + kf

    def set_debug(self, debug):
        self.debug = debug

    def set_status(self, status):
        self.show_print('settings status', status, debug=True)
        self.active = status
        if not status:
            self.hermes_weight = 0

    def set_avg_tara(self, avg_tara):
        try:
            self.avg_tara = int(avg_tara)
        except:
            self.show_print(self.avg_tara, '-  ЭТО НЕ ЧИСЛО')
            self.avg_tara = 0

    def set_max_brutto(self, max_brutto):
        try:
            self.max_brutto = int(max_brutto)
        except:
            self.show_print(self.max_brutto, '-  ЭТО НЕ ЧИСЛО')
            self.max_brutto = 0
        self.netto_max = self.max_brutto - self.avg_tara

    def send_data(self, data):
        data = self.make_magic(data)
        super().send_data(data)

    def set_avg_weigth(self, weight):
        try:
            self.avg_weight = int(weight)
        except:
            self.show_print(self.avg_weight, '-  ЭТО НЕ ЧИСЛО')
            self.avg_weight = 0

    def make_magic(self, data):
        if self.test_mode:
            print('\n[TEST] self.active', self.active)
            print('[TEST] isinstance(data, str)', isinstance(data, str))
            print('[TEST] isinstance(data, int)', isinstance(data, int))
            print('[TEST] self.avg_tara', self.avg_tara != 0)
            print('[TEST] self.max_brutto', self.max_brutto != 0)
            print('[TEST] self.avg_weight', self.avg_weight != 0)
            print('[TEST] int(data) > 300', int(data) > 300)
            print('[TEST] test_mode', self.test_mode)
        try:
            if self.active and (isinstance(data, str) or isinstance(data, int)) \
                    and self.avg_tara != 0 and \
                    self.max_brutto != 0 and self.avg_weight != 0 \
                    and int(data) > 300:
                print('\nHERMES WORK.\nDATA:{}'.format(data))
                data = int(data)
                if data < 0:
                    return str(data)
                # Вычитываем приблизительное (ожидаемое нетто)
                approx_netto = float(data) - float(self.avg_tara)
                self.notes = f'Ожидаемый вес ({approx_netto}) ||'
                if approx_netto < 0:
                    self.notes = 'Ожидаемое нетто ниже 0'
                    return str(data)
                self.show_print('approximate cargo is', approx_netto)
                # self.kf ~ 1.2. Получаем вес, который мы накинем на ожидаемое нетто
                delta_k = approx_netto * float(self.kf) - approx_netto
                self.show_print('new delta_k', delta_k)
                """ Проверяем не выше ли то, что мы накинем того, что мы накинули
                бы на средний вес """
                avg_delta = self.avg_weight * self.kf - self.avg_weight
                # if float(delta_k) > float(avg_delta):
                #    delta_k = float(avg_delta)
                self.show_print('avg_delta', avg_delta)

                # 6 положение (исключение отрицательного значения)
                delta_k = abs(delta_k)
                print('data', data)

                # 5 положение
                if int(delta_k) > 0:
                    new_data = float(data) + float(delta_k)
                    print('new_data', new_data)
                else:
                    new_data = data
                    self.notes += f'\nДельта около 0 ({delta_k}) ||'
                # 2 положение
                if float(new_data) > float(self.max_brutto):  # 2 Положение
                    print("NEW DATA", new_data)
                    print("MAX_BRUTTO", self.max_brutto)
                    self.notes += f"\nВес больше макс.брутто! ({self.max_brutto})"
                    new_data = data
                new_data = str(self.make_data_aliquot(new_data))
                print('New data', new_data)
                print('Old data', data)

                self.hermes_weight = int(new_data) - int(data)
                if int(new_data) < int(data):
                    new_data = data
                # Если то, что мы накинем, больше чем двойной кф, вернуть обычный
                if int(new_data) > (int(data) * self.kf):
                    self.notes = '\nНакидка больше, чем максимальная дельта по кф'
                    return str(data)
            else:
                new_data = str(data)
        except:
            new_data = str(data)
            self.show_print(format_exc())
            self.notes = 'Ошибка: {}'.format(format_exc())
        if self.test_mode:
            new_data = data
            self.notes += 'Тестовый режим'
        return str(new_data)

    def make_new_record(self, final: int, hermes: int = None):
        if not hermes:
            hermes = int(self.hermes_weight)
        try:
            db_funcs.create_new_record(record_id=self.record_id,
                                       clear_gross=final - hermes,
                                       hermes_gross=hermes,
                                       final_gross=final,
                                       test_mode=self.test_mode,
                                       notes=self.notes,
                                       kf_must_be=self.kf
                                       )
        except:
            print(format_exc())



    def make_netto_less(self, added, br_diff, kf):
        delta_k = added * kf
        if delta_k > br_diff:  # решить с кэфом
            over = delta_k - br_diff
            delta_k = delta_k - over * 1.1
        return delta_k
