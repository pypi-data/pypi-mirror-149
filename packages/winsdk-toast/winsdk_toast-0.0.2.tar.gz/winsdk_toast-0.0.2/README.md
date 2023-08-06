# winsdk_toast

A simple package for displaying Windows Toast Notification based on [winsdk].

Sometimes, after starting my data processing python script, I may surf the Internet.
It chokes my happiness that to frequently check whether the script stops,
or suddenly realize the script has stopped for a long while.

It'll be reassuring that the script can stop with a friendly gesture.


## Usage

```python
from os.path import abspath
from winsdk_toast import Notifier, Toast

path_pic = abspath('./example/resource/python.ico')

notifier = Notifier('程序名 applicationId')

# %% minimal example
toast = Toast()
toast.add_text('第一行 1st line')
notifier.show(toast)
# %% which is equivalent to
xml = """
<toast activationType="background">
    <visual>
        <binding template="ToastGeneric">
            <text>第一行 1st line</text>
        </binding>
    </visual>
</toast>
"""
toast = Toast(xml)
notifier.show(toast)


# %% simple example
toast = Toast()
toast.add_text('第一行 1st line', hint_align='center', hint_style='caption')
toast.add_text('第二行 2nd line')
toast.add_text('第三行 3rd line', placement='attribution')
toast.add_image(path_pic, placement='appLogoOverride')
toast.add_action('关闭 Close')
toast.set_audio(silent='true')
notifier.show(toast)
# %% which is equivalent to
xml = f"""
<toast activationType="background">
    <visual>
        <binding template="ToastGeneric">
            <text hint-style="caption" hint-align="center">第一行 1st line</text>
            <text>第二行 2nd line</text>
            <text placement="attribution">第三行 3rd line</text>
            <image src="{path_pic}" placement="appLogoOverride" />
        </binding>
    </visual>
    <actions>
        <action content="关闭 Close" arguments="dismiss" activationType="system" />
    </actions><audio loop="false" silent="true" />
</toast>
"""
toast = Toast(xml)
notifier.show(toast)

# %% example for control freak
toast = Toast()
element_toast = toast.set_toast(
    launch='blah', duration='long', displayTimeStamp='2022-04-01T12:00:00Z', scenario='default',
    useButtonStyle='false', activationType='background'
)
element_visual = toast.set_visual(
    version='1', lang='zh-CN', baseUri='ms-appx:///', branding='none', addImageQuery='false'
)
element_binding = toast.set_binding(
    template='ToastGeneric', fallback='2ndtemplate', lang='zh-CN', addImageQuery='false',
    baseUri='ms-appx:///', branding='none'
)
element_text = toast.add_text(
    text='第一行 1st line for control freak', id_='1', lang='zh-CN', placement=None,
    hint_maxLines='1', hint_style='title', hint_align='center', hint_wrap='false',
    element_parent=element_binding
)
element_group = toast.add_group()
element_subgroup_left = toast.add_subgroup(element_parent=element_group)
element_text = toast.add_text(
    text='第二行 2nd line for control freak', id_='2', lang='zh-CN', placement=None,
    hint_maxLines='1', hint_style='captionSubtle ', hint_align='left', hint_wrap='false',
    element_parent=element_subgroup_left
)
element_subgroup_right = toast.add_subgroup(element_parent=element_group)
element_text = toast.add_text(
    text='第三行 3rd line for control freak', id_='3', lang='zh-CN', placement='attribution',
    hint_maxLines='1', hint_style='captionSubtle', hint_align='left', hint_wrap='false',
    element_parent=element_subgroup_right
)
toast.add_image(
    path_pic, id_=None, alt='', addImageQuery='false',
    placement='appLogoOverride', hint_crop='circle'
)
toast.set_actions()
toast.add_action(
    '关闭 Close', arguments='dismiss', activationType='system', placement=None,
    imageUri=None, hint_inputId=None, hint_buttonStyle=None, hint_toolTip='tip close'
)
notifier.show(toast)
# %% which is equivalent to
xml = f"""
<toast launch="blah" duration="long" displayTimeStamp="2022-04-01T12:00:00Z" scenario="default" useButtonStyle="false" activationType="background">
    <visual version="1" lang="zh-CN" baseUri="ms-appx:///" branding="none" addImageQuery="false">
        <binding template="ToastGeneric" fallback="2ndtemplate" lang="zh-CN" addImageQuery="false" baseUri="ms-appx:///" branding="none">
            <text id="1" lang="zh-CN" hint-maxLines="1" hint-style="title" hint-align="center" hint-wrap="false">第一行 1st line for control freak</text>
            <group>
                <subgroup>
                    <text id="2" lang="zh-CN" hint-maxLines="1" hint-style="captionSubtle " hint-align="left" hint-wrap="false">第二行 2nd line for control freak</text>
                </subgroup>
                <subgroup>
                    <text id="3" lang="zh-CN" placement="attribution" hint-maxLines="1" hint-style="captionSubtle" hint-align="left" hint-wrap="false">第三行 3rd line for control freak</text>
                </subgroup>
            </group>
            <image src="{path_pic}" alt="" addImageQuery="false" placement="appLogoOverride" hint-crop="circle"/>
        </binding>
    </visual>
    <actions>
        <action content="关闭 Close" arguments="dismiss" activationType="system" hint-toolTip="tip close"/>
    </actions>
</toast>
"""
toast = Toast(xml)
notifier.show(toast)
```
The corresponding effects are like:

![minimal_example.gif](doc/pic/minimal_example.gif)

![simple_example.gif](doc/pic/simple_example.gif)

![example_for_control_freak.gif](doc/pic/example_for_control_freak.gif)


## Todo

- Events and callbacks.
- Documentation.
- Costume audio. According to [Microsoft Docs], this might be tricky.
- ...

[Microsoft Docs]: https://docs.microsoft.com/en-us/windows/apps/design/shell/tiles-and-notifications/custom-audio-on-toasts

## else

When I almost make it work, I found another package [windows_toast]
which has the same dependency and more features.
Luckily our 'styles' are quite different, and I'm on vacation,
so I decide to finish it any way.

If you need more features now, please use [windows_toast] instead,
maybe give this one a try later.

[winsdk]: https://pypi.org/project/winsdk
[windows_toast]: https://github.com/DatGuy1/Windows-Toasts
