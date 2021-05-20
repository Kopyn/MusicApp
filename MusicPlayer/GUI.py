from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import Test

class MainLayout(GridLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.rows = 1

        #Layouts
        self.navigationBar = BoxLayout(orientation = 'vertical')
        self.searchPanel = BoxLayout(orientation='vertical')
        self.playlistsPanel = BoxLayout(orientation='vertical')
        self.playerPanel = BoxLayout(orientation='horizontal')
        self.workspace = BoxLayout(orientation='vertical')

        #Customize and add navigation bar
        #self.anchorLayout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.searchButton = Button(text='Wyszukaj utwór', font_size=14)
        self.playlistsButton = Button(text='Biblioteka', font_size=14)
        self.navigationBar.add_widget(self.searchButton)
        self.navigationBar.add_widget(self.playlistsButton)
        self.searchButton.center_x = self.navigationBar.center_x
        self.searchButton.center_y = self.navigationBar.center_y
        #self.add_widget(self.anchorLayout)
        self.add_widget(self.navigationBar)

        #Add worspace panel
        self.add_widget(self.workspace)

        # Customize and add search panel
        self.searchInput = TextInput();
        self.searchPanel.add_widget(self.searchInput)
        self.workspace.add_widget(self.searchPanel)

        #Customize playlists panel


        #Customize and add player panel
        self.previousSong = Button(text='Previous', font_size=14)
        self.playerPanel.add_widget(self.previousSong)
        self.playButton = Button(text='Play', font_size=14)
        self.playButton.bind(on_press=self.playSong)
        self.playerPanel.add_widget(self.playButton)
        self.pauseButton = Button(text='Pause', font_size=14)
        self.pauseButton.bind(on_press=self.pauseSong)
        self.playerPanel.add_widget(self.pauseButton)
        self.nextSong = Button(text='Next', font_size=14)
        self.playerPanel.add_widget(self.nextSong)
        self.workspace.add_widget(self.playerPanel)



    def playSong(self, instance):
        Test.playSong()

    def pauseSong(self, instance):
        Test.pauseSong()



class MusicPlayer(Widget):
    def playSong(self, instance):
        Test.playSong()

    def pauseSong(self, instance):
        Test.pauseSong()

    def __init__(self, **kwargs):
        super(MusicPlayer, self).__init__(**kwargs)
        self.cols = 2
        #self.add_widget(NavigationBar())
        self.playButton = Button(text = 'Play', font_size = 14)
        self.playButton.bind(on_press = self.playSong)
        self.add_widget(self.playButton)
        self.pauseButton = Button(text = 'Pause', font_size = 14)
        self.pauseButton.bind(on_press = self.pauseSong)
        self.add_widget(Label(text = 'hiewrfddsfsdfdsgdfgfsdg'))
        self.add_widget(self.pauseButton)


class MusicApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    p = MusicApp()
    p.run()