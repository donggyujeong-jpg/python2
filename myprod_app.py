import sys
import sqlite3
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout,
    QMessageBox
)


DB_PATH = os.path.join(os.path.dirname(__file__), 'myprod.db')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MyProd 관리 (PyQt5)')
        self.conn = sqlite3.connect(DB_PATH)
        self.ensure_table()
        self.selected_id = None
        self.init_ui()
        self.load_data()

    def ensure_table(self):
        cur = self.conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS MyProd (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price INTEGER,
                qty INTEGER
            )
        ''')
        self.conn.commit()
        # 샘플 데이터가 없으면 100개 삽입
        cur.execute('SELECT COUNT(*) FROM MyProd')
        cnt = cur.fetchone()[0]
        if cnt == 0:
            self.generate_samples(100)

    def generate_samples(self, n):
        cur = self.conn.cursor()
        samples = []
        for i in range(1, n+1):
            name = f'제품 {i:03d}'
            price = (i * 123) % 50000 + 1000
            qty = (i * 7) % 200
            samples.append((name, price, qty))
        cur.executemany('INSERT INTO MyProd (name, price, qty) VALUES (?, ?, ?)', samples)
        self.conn.commit()

    def init_ui(self):
        w = QWidget()
        self.setCentralWidget(w)

        # 입력 라벨/필드
        lbl_name = QLabel('이름')
        self.txt_name = QLineEdit()
        lbl_price = QLabel('가격')
        self.spn_price = QSpinBox()
        self.spn_price.setRange(0, 100000000)
        lbl_qty = QLabel('수량')
        self.spn_qty = QSpinBox()
        self.spn_qty.setRange(0, 1000000)

        # 검색
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText('이름으로 검색')

        # 버튼
        btn_add = QPushButton('입력')
        btn_update = QPushButton('수정')
        btn_delete = QPushButton('삭제')
        btn_search = QPushButton('검색')

        btn_add.clicked.connect(self.on_add)
        btn_update.clicked.connect(self.on_update)
        btn_delete.clicked.connect(self.on_delete)
        btn_search.clicked.connect(self.on_search)

        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['id', 'name', 'price', 'qty'])
        self.table.cellClicked.connect(self.on_table_clicked)

        # 레이아웃 구성
        top_layout = QHBoxLayout()
        top_layout.addWidget(lbl_name)
        top_layout.addWidget(self.txt_name)
        top_layout.addWidget(lbl_price)
        top_layout.addWidget(self.spn_price)
        top_layout.addWidget(lbl_qty)
        top_layout.addWidget(self.spn_qty)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()
        btn_layout.addWidget(self.txt_search)
        btn_layout.addWidget(btn_search)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)

        w.setLayout(main_layout)

    def load_data(self, where=None, params=()):
        cur = self.conn.cursor()
        sql = 'SELECT id, name, price, qty FROM MyProd'
        if where:
            sql += ' WHERE ' + where
        sql += ' ORDER BY id'
        cur.execute(sql, params)
        rows = cur.fetchall()
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    def on_add(self):
        name = self.txt_name.text().strip()
        price = self.spn_price.value()
        qty = self.spn_qty.value()
        if not name:
            QMessageBox.warning(self, '입력 오류', '이름을 입력하세요.')
            return
        cur = self.conn.cursor()
        cur.execute('INSERT INTO MyProd (name, price, qty) VALUES (?, ?, ?)', (name, price, qty))
        self.conn.commit()
        self.load_data()
        self.clear_inputs()

    def on_update(self):
        if self.selected_id is None:
            QMessageBox.warning(self, '선택 오류', '수정할 행을 먼저 선택하세요.')
            return
        name = self.txt_name.text().strip()
        price = self.spn_price.value()
        qty = self.spn_qty.value()
        if not name:
            QMessageBox.warning(self, '입력 오류', '이름을 입력하세요.')
            return
        cur = self.conn.cursor()
        cur.execute('UPDATE MyProd SET name=?, price=?, qty=? WHERE id=?', (name, price, qty, self.selected_id))
        self.conn.commit()
        self.load_data()
        self.clear_inputs()

    def on_delete(self):
        if self.selected_id is None:
            QMessageBox.warning(self, '선택 오류', '삭제할 행을 먼저 선택하세요.')
            return
        ret = QMessageBox.question(self, '삭제 확인', '선택한 항목을 삭제하시겠습니까?')
        if ret == QMessageBox.Yes:
            cur = self.conn.cursor()
            cur.execute('DELETE FROM MyProd WHERE id=?', (self.selected_id,))
            self.conn.commit()
            self.load_data()
            self.clear_inputs()

    def on_search(self):
        term = self.txt_search.text().strip()
        if term == '':
            self.load_data()
        else:
            like = f'%{term}%'
            self.load_data('name LIKE ?', (like,))

    def on_table_clicked(self, row, column):
        item = self.table.item(row, 0)
        if item is None:
            return
        self.selected_id = int(self.table.item(row, 0).text())
        self.txt_name.setText(self.table.item(row, 1).text())
        self.spn_price.setValue(int(self.table.item(row, 2).text()))
        self.spn_qty.setValue(int(self.table.item(row, 3).text()))

    def clear_inputs(self):
        self.selected_id = None
        self.txt_name.clear()
        self.spn_price.setValue(0)
        self.spn_qty.setValue(0)

    def closeEvent(self, event):
        try:
            self.conn.close()
        except Exception:
            pass
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(900, 600)
    win.show()
    sys.exit(app.exec_())
