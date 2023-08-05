import sys
import logging
import json
import base64

from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA

sys.path.append('../../../messenger/')

from client_dist.client.client.main_window_conv import Ui_MainClientWindow
from client_dist.client.client.add_contact import AddContactDialog
from client_dist.client.client.del_contact import DelContactDialog
from client_dist.client.common.errors import ServerError
from client_dist.client.common.variables import *

logger = logging.getLogger('client_dist')


class ClientMainWindow(QMainWindow):
    """Класс главного окна, содержащий основную логику"""

    def __init__(self, database, transport, keys):
        super().__init__()
        self.database = database
        self.transport = transport
        self.decrypter = PKCS1_OAEP.new(keys)

        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)
        self.ui.menu_exit.triggered.connect(qApp.exit)
        self.ui.btn_send.clicked.connect(self.send_message)

        self.ui.smile1.clicked.connect(lambda: self.edit_message("\u2639"))
        self.ui.smile2.clicked.connect(lambda: self.edit_message("\u2620"))
        self.ui.smile3.clicked.connect(lambda: self.edit_message("\u2764"))

        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.menu_add_contact.triggered.connect(self.add_contact_window)

        self.ui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.ui.menu_del_contact.triggered.connect(self.delete_contact_window)

        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.current_chat_key = None
        self.encryptor = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)

        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)

        try:
            from PyQt5.QtWinExtras import QtWin
            self.myappid = 'mycompany.myproduct.subproduct.version'
            QtWin.setCurrentProcessExplicitAppUserModelID(self.myappid)
        except:
            pass
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QIcon('common/icon.png'))
        self.icon = QWidget()
        self.icon.setWindowIcon(QIcon('common/icon.png'))

        self.clients_list_update()
        self.set_disabled_input()
        self.show()

    def edit_message(self, smile):
        """Функция добавляет смайлики в окно ввода"""
        message_text = self.ui.text_message.toPlainText()
        new_text = message_text + smile
        self.ui.text_message.setText(new_text)

    def set_disabled_input(self):
        """Деквтиватор поля ввода"""
        self.ui.label_new_message.setText('Для выбора получателя дважды '
                                          'кликните на нем в окне контактов')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)

        self.encryptor = None
        self.current_chat = None
        self.current_chat_key = None

    def history_list_update(self):
        """Функция заполняет историю сообщений"""
        list_messages = sorted(self.database.get_history(self.current_chat),
                               key=lambda item: item[3])
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)
        self.history_model.clear()
        length = len(list_messages)
        start_index = 0
        if length > 20:
            start_index = length - 20

        for i in range(start_index, length):
            item = list_messages[i]
            if item[1] == 'in':
                mess = QStandardItem(
                    f'Входящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(255, 213, 213)))
                mess.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess)
            else:
                mess = QStandardItem(
                    f'Исходящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setTextAlignment(Qt.AlignRight)
                mess.setBackground(QBrush(QColor(204, 255, 204)))
                self.history_model.appendRow(mess)
        self.ui.list_messages.scrollToBottom()

    def select_active_user(self):
        """Функция обработчик двойного щелчка по контакту"""
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active_user()

    def set_active_user(self):
        """Функция устанавливающая активного собеседника"""
        try:
            self.current_chat_key = self.transport.key_request(self.current_chat)
            if self.current_chat_key:
                self.encryptor = PKCS1_OAEP.new(RSA.import_key(self.current_chat_key))
        except (OSError, json.JSONDecodeError):
            self.current_chat_key = None
            self.encryptor = None

        if not self.current_chat_key:
            self.messages.warning(
                self, 'Ошибка', 'Для выбранного пользователя нет ключа шифрования.')
            return

        self.ui.label_new_message.setText(f'Введите сообщение для {self.current_chat}:')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)

        self.history_list_update()

    def clients_list_update(self):
        """Функция обновления контакт-листа"""
        contacts_list = self.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def add_contact_window(self):
        """Функция добавления контакта"""
        global select_dialog
        select_dialog = AddContactDialog(self.transport, self.database)
        select_dialog.btn_ok.clicked.connect(lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, item):
        """Функция - обработчик добавления, сообщает серверу,
        обновляет таблицу и список контактов
        """
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, new_contact):
        """Функция добавляющая контакт в БД"""
        try:
            self.transport.add_contact(new_contact)
        except ServerError as err:
            self.messages.critical(self, 'Ошибка сервера', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.add_contact(new_contact)
            new_contact = QStandardItem(new_contact)
            new_contact.setEditable(False)
            self.contacts_model.appendRow(new_contact)
            logger.info(f'Успешно добавлен контакт {new_contact}')
            self.messages.information(self, 'Успех', 'Контакт успешно добавлен.')

    def delete_contact_window(self):
        """Функция удаления контакта"""
        global remove_dialog
        remove_dialog = DelContactDialog(self.database)
        remove_dialog.btn_ok.clicked.connect(lambda: self.delete_contact(remove_dialog))
        remove_dialog.show()

    def delete_contact(self, item):
        """Функция-обработчик удаления контакта: сообщает на сервер,
        обновляет таблицу контактов
        """
        selected = item.selector.currentText()
        try:
            self.transport.remove_contact(selected)
        except ServerError as err:
            self.messages.critical(self, 'Ошибка сервера', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.del_contact(selected)
            self.clients_list_update()
            logger.info(f'Успешно удалён контакт {selected}')
            self.messages.information(self, 'Успех', 'Контакт успешно удалён.')
            item.close()
            if selected == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    def send_message(self):
        """Функция отправки сообщения пользователю"""
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message_text:
            return
        message_text_encrypted = self.encryptor.encrypt(message_text.encode('utf8'))
        message_text_encrypted_base64 = base64.b64encode(message_text_encrypted)
        try:
            self.transport.send_message(self.current_chat, message_text_encrypted_base64.decode('ascii'))
            pass
        except ServerError as err:
            self.messages.critical(self, 'Ошибка', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
            self.close()
        else:
            self.database.save_message(self.current_chat, 'out', message_text)
            logger.debug(f'Отправлено сообщение для {self.current_chat}: {message_text}')
            self.history_list_update()

    @pyqtSlot(dict)
    def message(self, message):
        """Слот приёма нового сообщений"""
        encrypted_message = base64.b64decode(message[MESSAGE_TEXT])
        try:
            decrypted_message = self.decrypter.decrypt(encrypted_message)
        except (ValueError, TypeError):
            self.messages.warning(
                self, 'Ошибка', 'Не удалось декодировать сообщение.')
            return
        self.database.save_message(self.current_chat, 'in', decrypted_message.decode('utf8'))
        sender = message[SENDER]
        if sender == self.current_chat:
            self.history_list_update()
        else:
            if self.database.check_contact(sender):
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}, '
                                          f'открыть чат с ним?', QMessageBox.Yes,
                                          QMessageBox.No) == QMessageBox.Yes:
                    self.current_chat = sender
                    self.set_active_user()
            else:
                print('NO')
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}.\n '
                                          f'Данного пользователя нет в вашем контакт-листе.\n'
                                          f' Добавить в контакты и открыть чат с ним?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.database.save_message(self.current_chat, 'in', decrypted_message.decode('utf8'))
                    self.set_active_user()

    @pyqtSlot()
    def connection_lost(self):
        """Слот потери соединения
        Выдаёт сообщение об ошибке и завершает работу приложения
        """
        self.messages.warning(self, 'Сбой соединения', 'Потеряно соединение с сервером. ')
        self.close()

    @pyqtSlot()
    def sig_205(self):
        """Слот выполняющий обновление баз данных по команде сервера"""
        if self.current_chat and not self.database.check_user(
                self.current_chat):
            self.messages.warning(
                self,
                'Сочувствую',
                'К сожалению собеседник был удалён с сервера.')
            self.set_disabled_input()
            self.current_chat = None
        self.clients_list_update()

    def make_connection(self, trans_obj):
        """Функция соединения сигналов и слотов"""
        trans_obj.new_message.connect(self.message)
        trans_obj.connection_lost.connect(self.connection_lost)
        trans_obj.message_205.connect(self.sig_205)
