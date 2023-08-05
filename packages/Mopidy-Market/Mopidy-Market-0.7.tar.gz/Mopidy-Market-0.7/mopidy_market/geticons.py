import urllib.request
#      "jamendo":"https://images.jamendo.com/jamendomusic/static/svg/jamendo-music-logo-white.svg",
# https://www.radio.net/assets/images/logo/radio-net.png
# https://cms.tunein.com/wp-content/uploads/2018/02/primary.svg
icons = {
      "yamusic": "http://yastatic.net/s3/home/services/block/music_new.svg",
      "mpd": "http://www.musicpd.org/logo.png",
      "musicbox_darkclient": "https://github.com/stffart/mopidy-musicbox-webclient/raw/develop/screenshots/overview.png",
      "emby": "http://emby.media/favicon.ico",
      "bandcamp": "https://bandcamp.com/img/buttons/bandcamp-button-square-green-512.png",
      "beets": "https://user-images.githubusercontent.com/20903656/67691625-e2cfcf00-f9d9-11e9-821b-9cbdb7d8c332.png",
      "funkwhale" : "https://funkwhale.audio/img/logos/icon.svg",
      "internetarchive": "https://archive.org/download/InternetArchiveLogo/Internet%20Archive%20Logo.png",
      "dleyna": "https://images.squarespace-cdn.com/content/v1/54f08a57e4b0e91e31e8c76c/1427815734861-IX1OFBTFODTS57TXVP1M/DLNA_logo_color_big_white_text.png?format=1500w",
      "jellyfin":"https://jellyfin.org/images/banner-dark.svg",
      "mixcloud": "https://www.apkmirror.com/wp-content/themes/APKMirror/ap_resize/ap_resize.php?src=https%3A%2F%2Fwww.apkmirror.com%2Fwp-content%2Fuploads%2F2021%2F05%2F74%2F60a39672b6ed0.png&w=96&h=96&q=100",
      "orfradio": "https://upload.wikimedia.org/wikipedia/commons/d/dd/ORF_logo.svg",
      "pandora": "https://pandoragroup.com/-/media/images/media/logo/pandora_logo_blank.jpg",
      "podcast-itunes": "https://www.apple.com/v/itunes/home/k/images/overview/itunes_logo__dwjkvx332d0m_medium.png",
      "somafm": "https://somafm.com/img/LogoFP2010.gif",
      "soundcloud": "https://developers.soundcloud.com/assets/logo_big_white-65c2b096da68dd533db18b9f07d14054.png",
      "spotify": "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Green-768x231.png",
      "subidy":"http://www.subsonic.org/pages/inc/img/subsonic_logo.png",
      "youtube":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/1280px-YouTube_full-color_icon_%282017%29.svg.png",
      "ytmusic":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Youtube_Music_icon.svg/240px-Youtube_Music_icon.svg.png",
      "iris":"https://github.com/jaedb/Iris/raw/master/Screenshots/desktop-playlist.jpg",
      "mobile":"https://mopidy.com/media/ext/mobile.jpg",
      "mopster":"https://mopidy.com/media/ext/mopster.png",
      "mowecl":"https://mopidy.com/media/ext/mowecl.png",
      "muse":"https://mopidy.com/media/ext/muse.jpg",
      "musicbox_webclient":"https://mopidy.com/media/ext/musicbox-webclient.jpg",
      "party":"https://mopidy.com/media/ext/party.jpg",
      "mpris":"https://upload.wikimedia.org/wikipedia/commons/7/7b/Freedesktop-logo-for-template.svg",
      "alsamixer": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/ALSA_2019_logo.svg/374px-ALSA_2019_logo.svg.png",
      "nad":"https://nadelectronics.com/wp-content/themes/nad-theme/assets/img/svg/logo_red.svg"
}

newicons = {}

for c in icons:
  params1 = icons[c].split('?')
  params = params1[0].split('.')
  length = len(params)
  ext = params[length-1]
  print(c)
  print(icons[c])
  print(ext)
  filename = f"icons/{c}.{ext}"
  print(filename)
  newicons[c] = filename
  urllib.request.urlretrieve(icons[c], filename)

print(newicons)
