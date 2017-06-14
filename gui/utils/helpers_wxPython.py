# noinspection PyPackageRequirements
import wx

import gui.utils.colorUtils as colorUtils
from service.settings import GeneralSettings


def YesNoDialog(question=u'Are you sure you want to do this?', caption=u'Yes or no?'):
    dlg = wx.MessageDialog(None, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result


def OKDialog(question=u'Are you sure you want to do this?', caption=u'Yes or no?'):
    dlg = wx.MessageDialog(None, question, caption, wx.OK | wx.ICON_INFORMATION)
    result = dlg.ShowModal() == wx.ID_OK
    dlg.Destroy()
    return result


class PopupDialog(wx.Dialog):
    """ A popup dialog for temporary user messages """

    def __init__(self, parent, title, msg):
        # Create a dialog
        wx.Dialog.__init__(self, parent, -1, title, size=(350, 150), style=wx.CAPTION | wx.STAY_ON_TOP)
        # Add sizers
        box = wx.BoxSizer(wx.VERTICAL)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        # Add an Info graphic
        bitmap = wx.ArtProvider_GetBitmap(wx.ART_INFORMATION, wx.ART_MESSAGE_BOX, (32, 32))
        graphic = wx.StaticBitmap(self, -1, bitmap)
        box2.Add(graphic, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 10)
        # Add the message
        message = wx.StaticText(self, -1, msg)
        box2.Add(message, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        box.Add(box2, 0, wx.EXPAND)
        # Handle layout
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Fit()
        self.Layout()
        self.CentreOnScreen()
        # Display the Dialog
        self.Show()
        # Make sure the screen gets fully drawn before continuing.
        wx.Yield()


class Fonts(object):
    @staticmethod
    def getFont(FontType):
        size, family, style, weight = getattr(Fonts, FontType, Fonts.font_standard)
        return wx.Font(size, family, style, weight)

    general_settings = GeneralSettings.getInstance()

    font_standard = (
        general_settings.get('fontSize'),
        getattr(wx, 'FONTFAMILY_' + general_settings.get('fontType'), wx.FONTFAMILY_DEFAULT),
        getattr(wx, 'FONTSTYLE_' + general_settings.get('fontStyle'), wx.FONTSTYLE_NORMAL),
        getattr(wx, 'FONTWEIGHT_' + general_settings.get('fontWeight'), wx.FONTWEIGHT_NORMAL),
    )

    font_title_plus_one = (
        general_settings.get('fontSize') + 1,
        getattr(wx, 'FONTFAMILY_' + general_settings.get('fontType'), wx.FONTFAMILY_DEFAULT),
        getattr(wx, 'FONTSTYLE_' + general_settings.get('fontStyle'), wx.FONTSTYLE_NORMAL),
        wx.FONTWEIGHT_BOLD,
    )

    font_title_plus_two = (
        general_settings.get('fontSize') + 2,
        getattr(wx, 'FONTFAMILY_' + general_settings.get('fontType'), wx.FONTFAMILY_DEFAULT),
        getattr(wx, 'FONTSTYLE_' + general_settings.get('fontStyle'), wx.FONTSTYLE_NORMAL),
        wx.FONTWEIGHT_BOLD,
    )

    font_minus_one = (
        general_settings.get('fontSize') - 1,
        getattr(wx, 'FONTFAMILY_' + general_settings.get('fontType'), wx.FONTFAMILY_DEFAULT),
        getattr(wx, 'FONTSTYLE_' + general_settings.get('fontStyle'), wx.FONTSTYLE_NORMAL),
        getattr(wx, 'FONTWEIGHT_' + general_settings.get('fontWeight'), wx.FONTWEIGHT_NORMAL),
    )

    font_plus_one = (
        general_settings.get('fontSize') + 1,
        getattr(wx, 'FONTFAMILY_' + general_settings.get('fontType'), wx.FONTFAMILY_DEFAULT),
        getattr(wx, 'FONTSTYLE_' + general_settings.get('fontStyle'), wx.FONTSTYLE_NORMAL),
        getattr(wx, 'FONTWEIGHT_' + general_settings.get('fontWeight'), wx.FONTWEIGHT_NORMAL),
    )

    font_standard_bold = (
        general_settings.get('fontSize'),
        getattr(wx, 'FONTFAMILY_' + general_settings.get('fontType'), wx.FONTFAMILY_DEFAULT),
        getattr(wx, 'FONTSTYLE_' + general_settings.get('fontStyle'), wx.FONTSTYLE_NORMAL),
        wx.FONTWEIGHT_BOLD,
    )

    font_console = (
        general_settings.get('fontSize'),
        wx.FONTFAMILY_TELETYPE,
        getattr(wx, 'FONTSTYLE_' + general_settings.get('fontStyle'), wx.FONTSTYLE_NORMAL),
        getattr(wx, 'FONTWEIGHT_' + general_settings.get('fontWeight'), wx.FONTWEIGHT_NORMAL),
    )


class Frame(object):
    @staticmethod
    def ColorParser(color, default):
        # Check for valid color
        if color not in [
            'BLACK', 'BLUE', 'CYAN', 'GREEN', 'YELLOW', 'LIGHT_GREY', 'RED', 'WHITE', 'SYS_COLOUR_SCROLLBAR', 'SYS_COLOUR_BACKGROUND', 'SYS_COLOUR_ACTIVECAPTION',
            'SYS_COLOUR_INACTIVECAPTION', 'SYS_COLOUR_MENU', 'SYS_COLOUR_WINDOW', 'SYS_COLOUR_WINDOWFRAME', 'SYS_COLOUR_MENUTEXT', 'SYS_COLOUR_WINDOWTEXT',
            'SYS_COLOUR_CAPTIONTEXT', 'SYS_COLOUR_ACTIVEBORDER', 'SYS_COLOUR_INACTIVEBORDER', 'SYS_COLOUR_APPWORKSPACE', 'SYS_COLOUR_HIGHLIGHT',
            'SYS_COLOUR_HIGHLIGHTTEXT', 'SYS_COLOUR_BTNFACE', 'SYS_COLOUR_BTNSHADOW', 'SYS_COLOUR_GRAYTEXT', 'SYS_COLOUR_BTNTEXT', 'SYS_COLOUR_INACTIVECAPTIONTEXT',
            'SYS_COLOUR_BTNHIGHLIGHT', 'SYS_COLOUR_3DDKSHADOW', 'SYS_COLOUR_3DLIGHT', 'SYS_COLOUR_INFOTEXT', 'SYS_COLOUR_INFOBK', 'SYS_COLOUR_LISTBOX',
            'SYS_COLOUR_HOTLIGHT', 'SYS_COLOUR_GRADIENTACTIVECAPTION', 'SYS_COLOUR_GRADIENTINACTIVECAPTION', 'SYS_COLOUR_MENUHILIGHT', 'SYS_COLOUR_MENUBAR',
            'SYS_COLOUR_LISTBOXTEXT', 'SYS_COLOUR_LISTBOXHIGHLIGHTTEXT', 'SYS_COLOUR_MAX', 'SYS_COLOUR_DESKTOP', 'SYS_COLOUR_3DFACE', 'SYS_COLOUR_3DSHADOW',
            'SYS_COLOUR_BTNHILIGHT', 'SYS_COLOUR_3DHIGHLIGHT', 'SYS_COLOUR_3DHILIGHT', 'SYS_COLOUR_FRAMEBK'
        ]:
            color = 'BLACK'

        # Check for valid default colors
        # We use a limited list to make it simpler to handle compatibility
        if default not in ['BLACK', 'BLUE', 'CYAN', 'GREEN', 'YELLOW', 'LIGHT_GREY', 'RED', 'WHITE']:
            default = 'BLACK'

        if "SYS_COLOUR_" in color:
            color = wx.SystemSettings.GetColour(getattr(wx, color, getattr(wx, default)))
        else:
            color = getattr(wx, color, getattr(wx, default))

        return color

    @staticmethod
    def getBackgroundColor():
        general_settings = GeneralSettings.getInstance()
        color = Frame.ColorParser(general_settings.get('colorBackground'), 'LIGHT_GREY')

        return color

    @staticmethod
    def getBackgroundColorOffset(offsetby=.1, reverse=False):
        general_settings = GeneralSettings.getInstance()
        color = Frame.ColorParser(general_settings.get('colorBackground'), 'LIGHT_GREY')
        color = colorUtils.GetSuitableColor(color, offsetby, reverse)

        return color

    @staticmethod
    def getForegroundColor():
        general_settings = GeneralSettings.getInstance()
        color = Frame.ColorParser(general_settings.get('colorForeground'), 'BLACK')

        return color

    @staticmethod
    def getWarningColor():
        general_settings = GeneralSettings.getInstance()
        color = Frame.ColorParser(general_settings.get('colorWarning'), 'RED')

        return color


class DragDropHelper(object):
    data = None

    def __init__(self):
        pass
