# -*- coding: utf-8 -*-
import wx
import wx.grid
import random
import os
import pandas as pd
import time
from utils import Text2Voice

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, u'听写程序', size=(600, 600))
        cursor = wx.Cursor(wx.CURSOR_ARROW)
        self.SetCursor(cursor)
        self.menuBar = wx.MenuBar()
        self.panel = wx.Panel(self)
        self.SetBackgroundColour('White')
        self.statusbar = self.CreateStatusBar()

        font1 = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.font2 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.font3 = wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.font4 = wx.Font(11, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)

        toolbar = wx.ToolBar(self, -1, style=wx.TB_TEXT | wx.TB_NOICONS | wx.TB_DEFAULT_STYLE)
        self.ToolBar = toolbar
        upload = wx.NewIdRef(count=1)
        dictate = wx.NewIdRef(count=1)
        answer = wx.NewIdRef(count=1)
        instruction = wx.NewIdRef(count=1)
        author = wx.NewIdRef(count=1)
        tool1 = toolbar.AddRadioTool(upload, u'上传单词表', wx.Bitmap('./toolbar.jpg'))
        tool2 = toolbar.AddRadioTool(dictate, u'听写', wx.Bitmap('./toolbar.jpg'))
        tool3 = toolbar.AddRadioTool(answer, u'查看答案', wx.Bitmap('./toolbar.jpg'))
        tool4 = toolbar.AddTool(instruction, u'使用说明', wx.Bitmap('./toolbar.jpg'))
        tool5 = toolbar.AddTool(author, u'作者信息', wx.Bitmap('./toolbar.jpg'))
        toolbar.SetFont(font1)
        toolbar.Realize()

        self.ID_TIMER = 1
        self.timer = wx.Timer(self, self.ID_TIMER)
        self.ID_INTERVAL = 2
        self.timer_interval = wx.Timer(self, self.ID_INTERVAL)

        self.Bind(wx.EVT_TOOL, self.OnUpload, tool1)
        self.Bind(wx.EVT_TOOL, self.OnDictate, tool2)
        self.Bind(wx.EVT_TOOL, self.OnAnswer, tool3)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=self.ID_TIMER)
        self.Bind(wx.EVT_TIMER, self.OnTimer_Interval, id=self.ID_INTERVAL)
        self.Bind(wx.EVT_TOOL, self.OnHelpInstruction, tool4)
        self.Bind(wx.EVT_TOOL, self.OnHelpAuthor, tool5)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.if_upload = False
        self.input_path = ''
        self.has_title = True
        self.title = []
        self.language_list = ['中文', '英文', '日文']
        self.circle_list = [str(i) for i in range(1, 4)]
        self.interval_list = [str(i) + 's' for i in range(2, 6)]
        self.PlayOrder_list = ['顺序', '随机']
        self.language = '日文'
        self.circle = 2
        self.interval = 3
        self.PlayOrder = '随机'
        self.play_num = 0
        self.vocabulary_num = 0
        self.process_bar = 0
        self.index_list = []
        self.index = 0
        self.columns = 0

        # initialize
        hint = wx.StaticText(self.panel, -1, u'请上传单词表excel文件', pos=(20, 20))
        hint.SetFont(self.font2)
        info = wx.StaticText(self.panel, -1, u'行标题：', pos=(20, 60))
        info.SetFont(self.font3)
        self.radio1 = wx.RadioButton(self.panel, -1, u"有", (100, 60), style=wx.RB_GROUP)
        self.radio2 = wx.RadioButton(self.panel, -1, u"无", (150, 60))
        self.radio1.SetValue(True)

        okButton = wx.Button(self.panel, -1, u'上传', pos=(20, 100))
        self.Bind(wx.EVT_BUTTON, self.OnFileDialog, okButton)
        hint = wx.StaticText(self.panel, -1, u'状态：', pos=(20, 150))
        hint.SetFont(self.font2)
        state = wx.StaticText(self.panel, -1, u'未上传', pos=(100, 150))
        state.SetFont(self.font2)
        state.SetForegroundColour('Red')


    def OnUpload(self, event):
        self.timer.Stop()
        self.timer_interval.Stop()
        if self.index > 0:
            if self.index < len(self.index_list):
                self.statusbar.SetStatusText('paused')
            else:
                self.statusbar.SetStatusText('finish')
        try:
            if self.choice1:
                self.play = self.choice1.GetStringSelection()
                self.language = self.choice2.GetStringSelection()
                self.circle = int(self.choice3.GetStringSelection())
                self.interval = int(self.choice4.GetStringSelection()[0])
                self.PlayOrder = self.choice5.GetStringSelection()
        except:
            _ = -1
        for child in self.panel.GetChildren():
            child.Destroy()

        hint = wx.StaticText(self.panel, -1, u'请上传单词表excel文件', pos=(20, 20))
        hint.SetFont(self.font2)
        info = wx.StaticText(self.panel, -1, u'行标题：', pos=(20, 60))
        info.SetFont(self.font3)
        self.radio1 = wx.RadioButton(self.panel, -1, u"有", (100, 60), style=wx.RB_GROUP)
        self.radio2 = wx.RadioButton(self.panel, -1, u"无", (150, 60))
        if self.has_title:
            self.radio1.SetValue(True)
        else:
            self.radio2.SetValue(True)

        okButton = wx.Button(self.panel, -1, u'上传', pos=(20, 100))
        self.Bind(wx.EVT_BUTTON, self.OnFileDialog, okButton)
        hint = wx.StaticText(self.panel, -1, u'状态：', pos=(20, 150))
        hint.SetFont(self.font2)
        if self.if_upload:
            state = wx.StaticText(self.panel, -1, u'已上传', pos=(100, 150))
            state.SetFont(self.font2)
            state.SetForegroundColour('Blue')
        else:
            state = wx.StaticText(self.panel, -1, u'未上传', pos=(100, 150))
            state.SetFont(self.font2)
            state.SetForegroundColour('Red')
        # self.debug()

    def OnFileDialog(self, event):
        if self.radio1.GetValue() == True:
            self.has_title = True
        else:
            self.has_title = False
        wildcard = "Excel File (*.xlsx)|*.xlsx|" \
                   "Excel File 97-2003 (*.xls)|*.xls" \
                    # "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Choose a excel file", os.getcwd(), "", wildcard, wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.input_path = dialog.GetPath()
            if self.has_title:
                df = pd.read_excel(self.input_path)
                self.title = df.columns.values.tolist()
                self.play = self.title[0]
            else:
                df = pd.read_excel(self.input_path, header=None)
                self.title = ['单词', '释义']
                self.play = self.title[0]

            self.index_list = df.index.values.tolist()
            self.index = 0
            self.vocabulary = df.values
            self.vocabulary_num = len(self.index_list)
            self.columns = len(df.columns.values)
            self.process_bar = 0
            self.play_num = 0

            if self.if_upload:
                state = wx.StaticText(self.panel, -1, u'已重新上传', pos=(100, 150))
                state.SetFont(self.font2)
                state.SetForegroundColour('Blue')
            else:
                self.if_upload = True
                state = wx.StaticText(self.panel, -1, u'已上传', pos=(100, 150))
                state.SetFont(self.font2)
                state.SetForegroundColour('Blue')
        dialog.Destroy()


    def OnDictate(self, event):
        try:
            if self.radio1:
                if self.radio1.GetValue() == True:
                    self.has_title = True
                else:
                    self.has_title = False
        except:
            _ = -1

        for child in self.panel.GetChildren():
            child.Destroy()
        if self.index > 0:
            if self.index < len(self.index_list):
                self.statusbar.SetStatusText('paused')
            else:
                self.statusbar.SetStatusText('finish')

        info = wx.StaticText(self.panel, -1, u'播放：', pos=(20, 25))
        info.SetFont(self.font3)
        self.choice1 = wx.Choice(self.panel, choices=self.title, size=(80, -1), pos=(110, 20))
        if self.title:
            self.choice1.SetSelection(self.title.index(self.play))
        info = wx.StaticText(self.panel, -1, u'语言：', pos=(20, 65))
        info.SetFont(self.font3)
        self.choice2 = wx.Choice(self.panel, choices=self.language_list, size=(80, -1), pos=(110, 60))
        self.choice2.SetSelection(self.language_list.index(self.language))
        info = wx.StaticText(self.panel, -1, u'循环次数：', pos=(20, 105))
        info.SetFont(self.font3)
        self.choice3 = wx.Choice(self.panel, choices=self.circle_list, size=(80, -1), pos=(110, 100))
        self.choice3.SetSelection(self.circle - 1)
        info = wx.StaticText(self.panel, -1, u'间隔时间：', pos=(20, 145))
        info.SetFont(self.font3)
        self.choice4 = wx.Choice(self.panel, choices=self.interval_list, size=(80, -1), pos=(110, 140))
        self.choice4.SetSelection(self.interval - 2)
        info = wx.StaticText(self.panel, -1, u'播放顺序：', pos=(20, 185))
        info.SetFont(self.font3)
        self.choice5 = wx.Choice(self.panel, choices=self.PlayOrder_list, size=(80, -1), pos=(110, 180))
        self.choice5.SetSelection(self.PlayOrder_list.index(self.PlayOrder))

        okButton1 = wx.Button(self.panel, -1, u'开始', pos=(300, 20))
        self.Bind(wx.EVT_BUTTON, self.OnPlay, okButton1)
        okButton2 = wx.Button(self.panel, -1, u'暂停', pos=(300, 60))
        self.Bind(wx.EVT_BUTTON, self.OnPause, okButton2)
        okButton3 = wx.Button(self.panel, -1, u'重新开始', pos=(300, 100))
        self.Bind(wx.EVT_BUTTON, self.OnRestart, okButton3)

        info = wx.StaticText(self.panel, -1, u'听写进度：', pos=(300, 150))
        info.SetFont(self.font3)
        info = wx.StaticText(self.panel, -1, u'剩余单词：', pos=(300, 190))
        info.SetFont(self.font3)
        self.process_info = wx.TextCtrl(self.panel, -1, str(int(self.process_bar * 100)) + '%',
                                        size=(80, -1), style=wx.TE_READONLY, pos=(390, 145))
        self.process_info.SetFont(self.font4)
        self.remain_info = wx.TextCtrl(self.panel, -1, str(self.vocabulary_num - self.play_num),
                                        size=(80, -1), style=wx.TE_READONLY, pos=(390, 185))
        self.remain_info.SetFont(self.font4)
        # self.debug()


    def OnPlay(self, event):
        if self.title == []:
            wx.MessageBox(u'未上传单词表', u'ERROR', wx.OK | wx.ICON_INFORMATION, self)
            return
        if self.index and self.PlayOrder != self.choice5.GetStringSelection():
            wx.MessageBox(u'播放途中不能切换播放顺序，请点击重新开始', u'ERROR', wx.OK | wx.ICON_INFORMATION, self)
            return

        self.play = self.choice1.GetStringSelection()
        self.language = self.choice2.GetStringSelection()
        self.circle = int(self.choice3.GetStringSelection())
        self.interval = int(self.choice4.GetStringSelection()[0])
        self.PlayOrder = self.choice5.GetStringSelection()

        if self.index == 0:
            if self.PlayOrder == '顺序':
                self.index_list.sort()
            elif self.PlayOrder == '随机':
                random.shuffle(self.index_list)
        idx = self.title.index(self.play)
        self.play_list = self.vocabulary[:, idx]
        if self.language == '中文':
            self.lang = 'zh-cn'
        elif self.language == '英文':
            self.lang = 'en'
        elif self.language == '日文':
            self.lang = 'ja'
        self.idx_circle = 0
        self.idx_interval = 0

        self.timer.Start()
        self.statusbar.SetStatusText('playing...')

    def OnPause(self, event):
        if self.title == []:
            wx.MessageBox(u'未上传单词表', u'ERROR', wx.OK | wx.ICON_INFORMATION, self)
            return
        self.timer.Stop()
        self.timer_interval.Stop()
        self.statusbar.SetStatusText('paused')

    def OnRestart(self, event):
        if self.title == []:
            wx.MessageBox(u'未上传单词表', u'ERROR', wx.OK | wx.ICON_INFORMATION, self)
            return

        self.timer.Stop()
        self.timer_interval.Stop()

        self.play = self.choice1.GetStringSelection()
        self.language = self.choice2.GetStringSelection()
        self.circle = int(self.choice3.GetStringSelection())
        self.interval = int(self.choice4.GetStringSelection()[0])
        self.PlayOrder = self.choice5.GetStringSelection()

        self.index = 0
        if self.PlayOrder == '顺序':
            self.index_list.sort()
        elif self.PlayOrder == '随机':
            random.shuffle(self.index_list)
        idx = self.title.index(self.play)
        self.play_list = self.vocabulary[:, idx]
        if self.language == '中文':
            self.lang = 'zh-cn'
        elif self.language == '英文':
            self.lang = 'en'
        elif self.language == '日文':
            self.lang = 'ja'
        self.idx_circle = 0
        self.idx_interval = 0
        self.play_num = 0
        self.process_bar = 0
        self.process_info.SetValue(str(int(self.process_bar * 100)) + '%')
        self.remain_info.SetValue(str(self.vocabulary_num - self.play_num))

        self.timer.Start()
        self.statusbar.SetStatusText('playing...')

    def OnTimer(self, event):
        if event.GetId() == self.ID_TIMER:
            if self.index < len(self.index_list):
                Text2Voice(self.play_list[self.index_list[self.index]], self.lang)
                self.idx_circle += 1
                if self.idx_circle == self.circle:
                    self.index += 1
                    self.idx_circle = 0
                    self.play_num += 1
                    self.process_bar = float(self.play_num / self.vocabulary_num)
                    self.process_info.SetValue(str(int(self.process_bar * 100)) + '%')
                    self.remain_info.SetValue(str(self.vocabulary_num - self.play_num))
                self.timer.Stop()
                self.timer_interval.Start()
            else:
                self.statusbar.SetStatusText('finish')
        else:
            event.Skip()

    def OnTimer_Interval(self, event):
        if event.GetId() == self.ID_INTERVAL:
            time.sleep(1)
            self.idx_interval += 1
            if self.idx_interval == self.interval - 1:
                self.timer_interval.Stop()
                self.idx_interval = 0
                self.timer.Start()
        else:
            event.Skip()

    def OnAnswer(self, event):
        self.timer.Stop()
        self.timer_interval.Stop()
        if self.index > 0:
            if self.index < len(self.index_list):
                self.statusbar.SetStatusText('paused')
            else:
                self.statusbar.SetStatusText('finish')
        try:
            if self.choice1:
                self.play = self.choice1.GetStringSelection()
                self.language = self.choice2.GetStringSelection()
                self.circle = int(self.choice3.GetStringSelection())
                self.interval = int(self.choice4.GetStringSelection()[0])
                self.PlayOrder = self.choice5.GetStringSelection()
        except:
            _ = -1
        try:
            if self.radio1:
                if self.radio1.GetValue() == True:
                    self.has_title = True
                else:
                    self.has_title = False
        except:
            _ = -1
        for child in self.panel.GetChildren():
            child.Destroy()
        self.grid = wx.grid.Grid(self.panel, -1, pos=(10, 10), size=(560, 500), style=wx.WANTS_CHARS)
        self.grid.CreateGrid(self.index, self.columns)
        if self.if_upload:
            for i in range(len(self.title)):
                self.grid.SetColLabelValue(i, self.title[i])
                self.grid.SetColSize(i, 150)
        for r in range(self.index):
            for c in range(self.vocabulary.shape[1]):
                word = str(self.vocabulary[self.index_list[r], c])
                if word != 'nan':
                    self.grid.SetCellValue(r, c, word)
                    self.grid.SetReadOnly(r, c)
        # self.debug()

    def debug(self):
        print('==================')
        print('if_upload =', self.if_upload)
        print('input_path =', self.input_path)
        print('has_title =', self.has_title)
        print('title =', self.title)
        print('language =', self.language)
        print('circle =', self.circle)
        print('interval =', self.interval)
        print('PlayOrder =', self.PlayOrder)
        print('play_num =', self.play_num)
        print('vocabulary_num =', self.vocabulary_num)
        print('process_bar =', self.process_bar)
        print('index =', self.index)
        print('columns =', self.columns)

    def OnHelpInstruction(self, event):
        wx.MessageBox(u'使用说明指南\n\n· 上传单词表excel文件，默认第一列是单词，第二列是释义\n'
                      u'· 听写途中可以暂停，切换设置之后可以继续开始\n'
                      u'· 如中途切换播放顺序，需点击重新开始\n'
                      u'· 可随时查看当前已听写的内容\n',
                  u'听写程序', wx.OK | wx.ICON_INFORMATION, self)

    def OnHelpAuthor(self, event):
        wx.MessageBox(u'作者信息\n\nAUTHOR:    Niwako\nMAILBOX：grayniwako@gmail.com\n',
                  u'听写程序', wx.OK | wx.ICON_INFORMATION, self)

    def OnClose(self, event):
        dlg = wx.MessageDialog(None, u'确认离开？', u'关闭', wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            event.Skip()
            frame.Show(True)
        dlg.Destroy()
        fp = '.temp.mp3'
        if os.path.exists(fp):
            os.remove(fp)


if __name__ == u'__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Center(wx.BOTH)
    frame.Show(True)
    app.MainLoop()
