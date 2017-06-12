import gettext
gettext.find('myapplication', 'trans')
_ = gettext.gettext

# ...
print(_('This is a translatable string.'))
