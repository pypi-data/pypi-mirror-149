#!/bin/bash
# i18ndude should be available in current $PATH (eg by running
# ``export PATH=$PATH:$BUILDOUT_DIR/bin`` when i18ndude is located in your buildout's bin directory)
#
# For every language you want to translate into you need a
# locales/[language]/LC_MESSAGES/contenttypes.basic.po
# (e.g. locales/de/LC_MESSAGES/contenttypes.basic.po)

domain=contenttypes.basic
bin_path=/opt/Plone-5.2/zeocluster/bin
languages=("ca" "en" "es")

$bin_path/i18ndude rebuild-pot --pot $domain.pot --merge manual.pot --create $domain ../

for language in "${languages[@]}"
do
  if [ ! -e $language ]; then
    mkdir $language
  fi
  if [ ! -e $language/LC_MESSAGES ]; then
    mkdir $language/LC_MESSAGES
  fi
  if [ ! -e $language/LC_MESSAGES/$domain.po ]; then
    touch $language/LC_MESSAGES/$domain.po
  fi
  $bin_path/i18ndude sync --pot $domain.pot $language/LC_MESSAGES/$domain.po
done
