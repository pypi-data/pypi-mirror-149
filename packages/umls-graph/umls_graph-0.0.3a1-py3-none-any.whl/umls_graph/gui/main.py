import os
import pickle
import sys
import PyQt5
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QFileSystemModel, QTableWidgetItem, \
    QProgressBar
from quickcsv import *
import sys
import os
from umls_graph.gui.umls_main import Ui_MainWindow
from dask import dataframe as dd
import time

import ctypes
myappid = 'umls-graph-gui' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.data_path = "../../../examples/umls_datasets"
        if not os.path.exists(self.data_path):
            self.data_path="umls_datasets"
        self.dict_tables = {}
        self.current_path = os.path.dirname(__file__)
        if os.path.exists(self.current_path+"/umls_fields.pickle"):
            self.dict_tables=pickle.load(open(self.current_path+"/umls_fields.pickle","rb"))
        self.config={}
        if os.path.exists(self.data_path):
            for file in os.listdir(self.data_path):
                self.cb_tables.addItem(file)
            self.cb_table_changed()
        # self.load_datasets()
        # self.cb_tables.setCurrentIndex(0)
       #  self.cb_table_changed()
        self.btn_search.clicked.connect(self.search)
        if os.path.exists(self.current_path+"/umls_datasets"):
            self.edit_datapath.setText(self.current_path+"/umls_datasets")
        # else:
        #     self.edit_datapath.setText("")
        self.edit_datapath.setText(self.data_path)
        self.cb_tables.currentIndexChanged.connect(self.cb_table_changed)
        self.btn_load_datasets.clicked.connect(self.load_datasets)
        self.pbar = QProgressBar(self)
        self.layout_progress.addWidget(self.pbar)
        self.btn_select_datafolder.clicked.connect(self.select_datafolder)
        self.btn_associate.clicked.connect(self.associate_concept)
        self.btn_first10.clicked.connect(self.first10)
        self.tv_results.itemSelectionChanged.connect(self.select_changed)
        self.tv_result_rel.itemSelectionChanged.connect(self.select_changed_rel)
        self.btn_export.clicked.connect(self.export)

        rel_tables=['umls_rels.csv','umls_atui_rels.csv','umls_sty_rels.csv','umls_smap_rels.csv','umls_ambig_lui.csv','umls_ambig_lui.csv',
                    'umls_def_rels.csv'
                    ]
        for r in rel_tables:
            self.cb_rel_tables.addItem(r)
        self.cb_rel_tables.setCurrentIndex(0)

    def export(self):
        list_values = []
        for item in self.tv_results.selectedItems():
            # print(item.row(), item.column(), item.text())
            list_values.append(item.text())
        if len(list_values) == 1:
            selected_id = list_values[0]
            rel_csv_file=self.cb_rel_tables.currentText()
            self.pbar.setValue(0)
            QMessageBox.information(self,"选择",f"导出到当前目录：kg_{selected_id}.csv")
            if selected_id.startswith("C") or selected_id.startswith("A") or selected_id.startswith("L") or selected_id.startswith("S"):
                list_rel=[]
                list_concept=self.find_concepts(rel_csv_file,selected_id)
                self.pbar.setMaximum(len(list_concept))
                for idx,concept in enumerate(list_concept):
                    print(concept)
                    if ":END_ID" in concept:
                        next_id=concept[":END_ID"]
                        list_rel.append({
                            "source":selected_id,
                            "relation":concept["RELA"],
                            "relation_type":concept[":TYPE"],
                            "relation_id": concept["RUI"],
                            "sab":concept["SAB"],
                            "target":next_id
                        })
                        list_next_model = self.find_concepts(rel_csv_file, next_id)
                        for idx1, concept1 in enumerate(list_next_model):
                            print(concept1)
                            if ":END_ID" in concept1:
                                next_id1 = concept1[":END_ID"]
                                list_rel.append({
                                    "source": next_id,
                                    "relation": concept1["RELA"],
                                    "relation_type": concept1[":TYPE"],
                                    "relation_id":concept1["RUI"],
                                    "sab": concept1["SAB"],
                                    "target": next_id1
                                })
                                '''
                                list_next_model2 = self.find_concepts(rel_csv_file, next_id1)
                                for idx2, concept2 in enumerate(list_next_model2):
                                    print(concept1)
                                    if ":END_ID" in concept2:
                                        next_id2 = concept2[":END_ID"]
                                        list_rel.append({
                                            "source": next_id1,
                                            "relation": concept2["RELA"],
                                            "target": next_id2
                                        })
                                '''
                    self.pbar.setValue(idx+1)
                self.pbar.setValue(self.pbar.maximum())
                # save data
                if len(list_rel)!=0:
                    write_csv(f"kg-{selected_id}-{rel_csv_file}",list_rel)
                    QMessageBox.about(self, "提示", "完成导出！")
                else:
                    QMessageBox.about(self, "提示", "无输出结果！")
                self.lb_export_info.setText(f"Finished!")
        else:
            QMessageBox.about(self,"提示","请选择一个有效的概念ID")

    def select_changed(self):
        try:
            row_index=self.tv_results.currentRow()
            cols=self.tv_results.columnCount()
            show_text=""
            show_label=""
            if cols <=0:
                self.edit_show.setText("")
                return
            for c in range(cols):
                h=self.tv_results.horizontalHeaderItem(c)
                # print(h.text())
                item=self.tv_results.item(row_index,c)
                # print(item.text())
                if h.text() in ['STR','DEF','STR_RL','STY','EXPR']:
                    show_label=h.text()
                    show_text=item.text()
            if show_label!="":
                self.edit_show.setText(f"{show_label}: {show_text}")
            else:
                self.edit_show.setText("")
        except Exception as err:
            print(err)
        # print()

    def select_changed_rel(self):
        try:
            row_index=self.tv_result_rel.currentRow()
            cols=self.tv_result_rel.columnCount()
            show_text=""
            show_label=""
            if cols <=0:
                self.edit_show.setText("")
                return
            for c in range(cols):
                h=self.tv_result_rel.horizontalHeaderItem(c)
                # print(h.text())
                item=self.tv_result_rel.item(row_index,c)
                # print(item.text())
                if h.text() in ['STR','DEF','STR_RL','STY','EXPR']:
                    show_label=h.text()
                    show_text=item.text()
            if show_label!="":
                self.edit_show.setText(f"{show_label}: {show_text}")
            else:
                self.edit_show.setText("")
        except Exception as err:
            print(err)
        # print()

    def find_concepts(self,rel_csv_file,selected_id):
        select_csv_path = self.data_path + "/" + rel_csv_file
        better_dtypes = {}
        for t in self.dict_tables[rel_csv_file]:
            better_dtypes[t] = "string"
        dask_df = dd.read_csv(select_csv_path, dtype=better_dtypes, low_memory=False)
        cols = list(dask_df.columns.values)
        print(cols)
        result = dask_df.query(f"`:START_ID` == \"{selected_id}\"")
        print("Finding records from resulting partitions...")
        num_partitions = len(result.divisions)
        print("partitions:", result.partitions)
        # self.pbar.setValue(0)
        # self.pbar.setMaximum(num_partitions)
        count = 0
        list_all_model = []
        self.lb_export_info.setText(f"Exporting...{selected_id}")
        for part in result.partitions:
            start1 = time.time()
            part_df = part.compute()
            list_model = []
            c = len(part_df)
            end1 = time.time()
            print(f"Part: {count}")
            print(f"Part Size:  {c}, Time: {(end1 - start1)} sec")
            count += 1
            for index, row in part_df.iterrows():
                model = {}
                for k in cols:
                    v = row[k]
                    if str(type(v)) != "str":
                        v = str(v)
                    model[k] = v
                list_model.append(model)
            list_all_model += list_model
            # print(list_model)
            # self.pbar.setValue(count)

            print(list_model)
            QApplication.processEvents()

            print()
        # self.pbar.setValue(self.pbar.maximum())
        print(list_all_model)
        return list_all_model



    def first10(self):
        self.search_all(head_num=10)

    def associate_concept(self):
        list_values=[]
        for item in self.tv_results.selectedItems():
            print(item.row(), item.column(), item.text())
            list_values.append(item.text())
        if len(list_values)>0:
            selected_id=list_values[0]
            if selected_id.startswith("C") or selected_id.startswith("A") or selected_id.startswith("L") or selected_id.startswith("S"):
                # begin search
                self.tv_result_rel.clear()
                # find relationships
                # rel_csv_file="umls_rels.csv"
                rel_csv_file=self.cb_rel_tables.currentText()
                select_csv_path = self.data_path + "/" + rel_csv_file
                if not os.path.exists(select_csv_path):
                    QMessageBox.about(self, "提示", f"关系表{rel_csv_file}不存在!")
                    return
                better_dtypes = {}
                for t in self.dict_tables[rel_csv_file]:
                    better_dtypes[t] = "string"
                dask_df = dd.read_csv(select_csv_path, dtype=better_dtypes, low_memory=False)
                cols = list(dask_df.columns.values)
                print(cols)
                result = dask_df.query(f"`:START_ID` == \"{selected_id}\"")
                print("Finding records from resulting partitions...")
                num_partitions = len(result.divisions)
                print("partitions:", result.partitions)
                self.pbar.setMaximum(num_partitions)
                count = 0
                list_all_model = []
                for part in result.partitions:
                    start1 = time.time()
                    part_df = part.compute()
                    list_model = []
                    c = len(part_df)
                    end1 = time.time()
                    print(f"Part: {count}")
                    print(f"Part Size:  {c}, Time: {(end1 - start1)} sec")
                    count += 1
                    for index, row in part_df.iterrows():
                        model = {}
                        for k in cols:
                            v = row[k]
                            if str(type(v)) != "str":
                                v = str(v)
                            model[k] = v
                        list_model.append(model)
                    list_all_model += list_model
                    # print(list_model)
                    self.pbar.setValue(count)
                    print(list_model)
                    QApplication.processEvents()
                    print()
                print(list_all_model)
                # show results
                self.tv_result_rel.clear()
                self.tv_result_rel.setColumnCount(len(cols))
                self.tv_result_rel.setRowCount(len(list_all_model))
                self.tv_result_rel.setHorizontalHeaderLabels(cols)
                for idx, item in enumerate(list_all_model):
                    for idx1, k in enumerate(list(item.keys())):
                        newItem = QTableWidgetItem(item[k])
                        self.tv_result_rel.setItem(idx, idx1, newItem)
                self.pbar.setValue(self.pbar.maximum())
                QMessageBox.about(self, "提示", "已关联！")


    def select_datafolder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择数据文件夹', '', )
        if folder != ('', ''):
            print("output folder path : " + folder)
            if os.path.exists(folder):
                self.edit_datapath.setText(folder)
            else:
                QMessageBox.about(self, "提示", "请选择一个文件夹!")

    def load_datasets(self):
        self.data_path=self.edit_datapath.text()
        self.cb_tables.clear()
        self.cb_fields.clear()
        self.dict_tables={}
        for file in os.listdir(self.data_path):
            self.cb_tables.addItem(file)
            select_csv_path = self.data_path + "/" + file
            dask_df = dd.read_csv(select_csv_path)
            cols = dask_df.columns.values
            self.dict_tables[file] = cols
        pickle.dump(self.dict_tables, open(self.current_path+"/umls_fields.pickle", "wb"))

        QMessageBox.about(self, "提示", "加载完成!")


    def cb_table_changed(self):
        # QMessageBox.about(self, "提示",self.cb_tables.currentText())
        selected_field=self.cb_tables.currentText()
        if selected_field=="":
            return
        if selected_field not in self.dict_tables:
            select_csv_path = self.data_path + "/" + selected_field
            dask_df = dd.read_csv(select_csv_path)
            cols = list(dask_df)
            self.dict_tables[selected_field]=cols
        self.cb_fields.clear()
        if selected_field in self.dict_tables:
            for c in self.dict_tables[selected_field]:
                self.cb_fields.addItem(c)
            if self.cb_fields.count()>0:
                self.cb_fields.setCurrentIndex(0)

    def check_data(self):
        QMessageBox.about(self, "提示", "正在搜索...")

        pass

    def search(self):
        self.search_all()

    def search_all(self,head_num=-1):
        try:

            if not os.path.exists(self.edit_datapath.text()):
                QMessageBox.about(self, "错误提示", "数据集文件夹路径不存在！")
                return
            self.data_path=self.edit_datapath.text()



            self.pbar.setValue(0)
            self.tv_results.clear()

            # C0029942
            value=self.edit_search.text()
            select_csv_path = self.data_path + "/" + self.cb_tables.currentText()
            start = time.time()

            better_dtypes = {

            }
            for t in self.dict_tables[self.cb_tables.currentText()]:
                better_dtypes[t]="string"

            dask_df = dd.read_csv(select_csv_path,dtype=better_dtypes,low_memory=False)
            end = time.time()
            print("Read csv with dask: ", (end - start), "sec")
            cols=list(dask_df.columns.values)
            print(cols)

            list_all_model = []

            print("result:")
            print("head_num: ",head_num)
            if head_num==-1:
                # 普通查找
                if self.edit_search.text() == "":
                    QMessageBox.about(self, "错误提示", "请输入检索数据！")
                    return
                label=self.cb_fields.currentText().strip()
                print(f"label: {label}")
                print(f"value: {value}")
                if self.cb_vague.isChecked():
                    result = dask_df.query(f"`{label}`.str.contains(\"{value}\")",local_dict={"label":label,"value":value},engine="python")
                else:
                    result=dask_df.query(f"`{label}` == \"{value}\"",local_dict={"label":label,"value":value})
                end = time.time()
                print("query time: ", (end - start), "sec")



                count = 0
                start = time.time()
                print("Finding records from resulting partitions...")
                num_partitions = len(result.divisions)
                print("partitions:", result.partitions)
                self.pbar.setMaximum(num_partitions)
                for part in result.partitions:

                    start1 = time.time()
                    part_df = part.compute()
                    list_model = []
                    c = len(part_df)
                    end1 = time.time()
                    print(f"Part: {count}")
                    print(f"Part Size:  {c}, Time: {(end1 - start1)} sec")
                    count += 1
                    for index, row in part_df.iterrows():
                        model = {}
                        for k in cols:
                            v = row[k]
                            if str(type(v)) != "str":
                                v = str(v)
                            model[k] = v
                        list_model.append(model)
                    list_all_model += list_model
                    # print(list_model)
                    self.pbar.setValue(count)
                    print(list_model)
                    QApplication.processEvents()
                    print()
                print(list_all_model)
                end = time.time()
                print("find partitions time: ", (end - start), "sec")
                print(list_all_model)
            else:
                # 返回前10行
                result=dask_df.head(n=head_num)
                list_all_model=[]
                for index, row in result.iterrows():
                    model = {}
                    for k in cols:
                        v = row[k]
                        if str(type(v)) != "str":
                            v = str(v)
                        model[k] = v
                    list_all_model.append(model)

            # show results
            self.tv_results.clear()
            self.tv_results.setColumnCount(len(cols))
            self.tv_results.setRowCount(len(list_all_model))
            self.tv_results.setHorizontalHeaderLabels(cols)
            for idx, item in enumerate(list_all_model):
                for idx1, k in enumerate(list(item.keys())):
                    newItem = QTableWidgetItem(item[k])
                    self.tv_results.setItem(idx, idx1, newItem)

        except Exception as err:
            print(err)
        self.pbar.setValue(self.pbar.maximum())
        QMessageBox.about(self, "提示", "已搜索完！")
        print()

def main():
    app = QApplication(sys.argv)

    current_path = os.path.dirname(__file__)
    print("current path = ", current_path)

    myWin = MyMainForm()
    myWin.show()
    try:
        r = app.exec_()
    except Exception as err:
        print(err)

if __name__ == "__main__":
   main()