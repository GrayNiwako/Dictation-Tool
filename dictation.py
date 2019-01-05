# -*- coding: utf-8 -*-
import wx
import random

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, u'日语假名听写', size=(400, 600))
        cursor = wx.Cursor(wx.CURSOR_ARROW)
        self.SetCursor(cursor)
        self.menuBar = wx.MenuBar()
        self.panel = wx.Panel(self)
        self.SetBackgroundColour('White')
        self.statusbar = self.CreateStatusBar()

        About = wx.Menu()
        Instruction = wx.NewId()
        Author = wx.NewId()
        About.Append(Instruction, u'使用说明(&I)\tF1', u'使用说明指南')
        About.Append(Author, u'作者(&A)\tF2', u'作者信息')
        self.Bind(wx.EVT_MENU, self.OnHelpInstruction, id=Instruction)
        self.Bind(wx.EVT_MENU, self.OnHelpAuthor, id=Author)
        self.menuBar.Append(About, u'关于(&B)')
        self.SetMenuBar(self.menuBar)

        self.dictation = wx.TextCtrl(self.panel, -1, '', size=(85, -1), style=wx.TE_RICH | wx.TE_READONLY
                                                                             | wx.HSCROLL, pos=(30, 20))
        self.type = wx.TextCtrl(self.panel, -1, '', size=(85, -1), style=wx.TE_RICH | wx.TE_READONLY
                                                                               | wx.HSCROLL, pos=(30, 60))
        self.answer = wx.TextCtrl(self.panel, -1, '', size=(190, 470), style=wx.TE_MULTILINE | wx.TE_READONLY,
                                  pos=(160, 20))

        font1 = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.dictation.SetFont(font1)
        self.type.SetFont(font1)
        self.answer.SetFont(font1)

        Button1 = wx.Button(self.panel, -1, u'听写', pos=(30, 100))
        Button2 = wx.Button(self.panel, -1, u'答案', pos=(30, 140))
        Button3 = wx.Button(self.panel, -1, u'重置', pos=(30, 180))
        self.Bind(wx.EVT_BUTTON, self.OnDictate, Button1)
        self.Bind(wx.EVT_BUTTON, self.OnAnswer, Button2)
        self.Bind(wx.EVT_BUTTON, self.OnReset, Button3)

        self.my_word_list = []

        self.type_list = [u'平假名', u'片假名']
        self.word_list = ['a', 'i', 'u', 'e', u'o (あ行)',
                          'ka', 'ki', 'ku', 'ke', 'ko',
                          'sa', 'shi', 'su', 'se', 'so',
                          'ta', 'chi', 'tsu', 'te', 'to',
                          'na', 'ni', 'nu', 'ne', 'no',
                          'ha', 'hi', 'fu', 'he', 'ho',
                          'ma', 'mi', 'mu', 'me', 'mo',
                          'ya', 'yu', 'yo',
                          'ra', 'ri', 'ru', 're', 'ro',
                          'wa', u'o (わ行)', 'n',
                          'ga', 'gi', 'gu', 'ge', 'go',
                          'za', u'ji (ざ行)', u'zu (ざ行)', 'ze', 'zo',
                          'da', u'ji (だ行)', u'zu (だ行)', 'de', 'do',
                          'ba', 'bi', 'bu', 'be', 'bo',
                          'pa', 'pi', 'pu', 'pe', 'po',
                          'kya', 'kyu', 'kyo',
                          'sha', 'shu', 'sho',
                          'cha', 'chu', 'cho',
                          'nya', 'nyu', 'nyo',
                          'hya', 'hyu', 'hyo',
                          'mya', 'myu', 'myo',
                          'rya', 'ryu', 'ryo',
                          'gya', 'gyu', 'gyo',
                          'ja', 'ju', 'jo',
                          'bya', 'byu', 'byo',
                          'pya', 'pyu', 'pyo']
        self.word_dict = {'a':[u'あ',u'ア'], 'i':[u'い',u'イ'], 'u':[u'う',u'ウ'], 'e':[u'え',u'エ'], u'o (あ行)':[u'お',u'オ'],
                          'ka':[u'か',u'カ'], 'ki':[u'き',u'キ'], 'ku':[u'く',u'ク'], 'ke':[u'け',u'ケ'], 'ko':[u'こ',u'コ'],
                          'sa':[u'さ',u'サ'], 'shi':[u'し',u'シ'], 'su':[u'す',u'ス'], 'se':[u'せ',u'セ'], 'so':[u'そ',u'ソ'],
                          'ta':[u'た',u'タ'], 'chi':[u'ち',u'チ'], 'tsu':[u'つ',u'ツ'], 'te':[u'て',u'テ'], 'to':[u'と',u'ト'],
                          'na':[u'な',u'ナ'], 'ni':[u'に',u'ニ'], 'nu':[u'ぬ',u'ヌ'], 'ne':[u'ね',u'ネ'], 'no':[u'の',u'ノ'],
                          'ha':[u'は',u'ハ'], 'hi':[u'ひ',u'ヒ'], 'fu':[u'ふ',u'フ'], 'he':[u'へ',u'ヘ'], 'ho':[u'ほ',u'ホ'],
                          'ma':[u'ま',u'マ'], 'mi':[u'み',u'ミ'], 'mu':[u'む',u'ム'], 'me':[u'め',u'メ'], 'mo':[u'も',u'モ'],
                          'ya':[u'や',u'ヤ'], 'yu':[u'ゆ',u'ユ'], 'yo':[u'よ',u'ヨ'],
                          'ra':[u'ら',u'ラ'], 'ri':[u'り',u'リ'], 'ru':[u'る',u'ル'], 're':[u'れ',u'レ'], 'ro':[u'ろ',u'ロ'],
                          'wa':[u'わ',u'ワ'], u'o (わ行)':[u'を',u'ヲ'], 'n':[u'ん',u'ン'],
                          'ga':[u'が',u'ガ'], 'gi':[u'ぎ',u'ギ'], 'gu':[u'ぐ',u'グ'], 'ge':[u'げ',u'ゲ'], 'go':[u'ご',u'ゴ'],
                          'za':[u'ざ',u'ザ'], u'ji (ざ行)':[u'じ',u'ジ'], u'zu (ざ行)':[u'ず',u'ズ'], 'ze':[u'ぜ',u'ゼ'], 'zo':[u'ぞ',u'ゾ'],
                          'da':[u'だ',u'ダ'], u'ji (だ行)':[u'ぢ',u'ヂ'], u'zu (だ行)':[u'づ',u'ヅ'], 'de':[u'で',u'デ'], 'do':[u'ど',u'ド'],
                          'ba':[u'ば',u'バ'], 'bi':[u'び',u'ビ'], 'bu':[u'ぶ',u'ブ'], 'be':[u'べ',u'ベ'], 'bo':[u'ぼ',u'ボ'],
                          'pa':[u'ぱ',u'パ'], 'pi':[u'ぴ',u'ピ'], 'pu':[u'ぷ',u'プ'], 'pe':[u'ぺ',u'ペ'], 'po':[u'ぽ',u'ポ'],
                          'kya':[u'きゃ',u'キャ'], 'kyu':[u'きゅ',u'キュ'], 'kyo':[u'きょ',u'キョ'],
                          'sha':[u'しゃ',u'シャ'], 'shu':[u'しゅ',u'シュ'], 'sho':[u'しょ',u'ショ'],
                          'cha':[u'ちゃ',u'チャ'], 'chu':[u'ちゅ',u'チュ'], 'cho':[u'ちょ',u'チョ'],
                          'nya':[u'にゃ',u'ニャ'], 'nyu':[u'にゅ',u'ニュ'], 'nyo':[u'にょ',u'ニョ'],
                          'hya':[u'ひゃ',u'ヒャ'], 'hyu':[u'ひゅ',u'ヒュ'], 'hyo':[u'ひょ',u'ヒョ'],
                          'mya':[u'みゃ',u'ミャ'], 'myu':[u'みゅ',u'ミュ'], 'myo':[u'みょ',u'ミョ'],
                          'rya':[u'りゃ',u'リャ'], 'ryu':[u'りゅ',u'リュ'], 'ryo':[u'りょ',u'リョ'],
                          'gya':[u'ぎゃ',u'ギャ'], 'gyu':[u'ぎゅ',u'ギュ'], 'gyo':[u'ぎょ',u'ギョ'],
                          'ja':[u'じゃ',u'ジャ'], 'ju':[u'じゅ',u'ジュ'], 'jo':[u'じょ',u'ジョ'],
                          'bya':[u'びゃ',u'ビャ'], 'byu':[u'びゅ',u'ビュ'], 'byo':[u'びょ',u'ビョ'],
                          'pya':[u'ぴゃ',u'ピャ'], 'pyu':[u'ぴゅ',u'ピュ'], 'pyo':[u'ぴょ',u'ピョ']}

    def OnDictate(self, evt):
        cur_word = random.randint(0, len(self.word_list)-1)
        cur_type = random.randint(0, 1)
        self.dictation.SetValue(self.word_list[cur_word])
        self.type.SetValue(self.type_list[cur_type])
        self.my_word_list.append(self.word_dict[self.word_list[cur_word]][cur_type])

    def OnAnswer(self, evt):
        answer_list = ''
        for i in range(len(self.my_word_list)):
            answer_list += str(i+1) + '\t' + self.my_word_list[i] + '\n'
        self.answer.SetValue(answer_list)

    def OnReset(self, evt):
        self.dictation.Clear()
        self.type.Clear()
        self.answer.Clear()
        self.my_word_list.clear()

    def OnHelpInstruction(self, evt):
        wx.MessageBox(u'使用说明指南\n\n1. 点击“听写”按钮，显示随机罗马音和假名种类\n'
                      u'2. 点击“答案”按钮，右边框中显示答案\n'
                      u'3. 继续听写只需要多次点击“听写”按钮\n'
                      u'4. 点击“重置”按钮可以清空当前已听写内容\n',
                  u'日语假名听写', wx.OK | wx.ICON_INFORMATION, self)

    def OnHelpAuthor(self, evt):
        wx.MessageBox(u'作者信息\n\nCN：Niwako\nMAILBOX：grayniwako@foxmail.com\n',
                  u'日语假名听写', wx.OK | wx.ICON_INFORMATION, self)

if __name__ == u'__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show(True)
    frame.Center(wx.BOTH)
    app.MainLoop()
