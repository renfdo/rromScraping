import rom.game as g
import rom.console as c
import boto3
import rom.request as req

def all():
    console = None
    console = c.consoleList("https://romsmania.com/", "/search?orderAsc=1&page=1").getConsole("Super Nintendo")

    console.run(True)
    console.to_s3()


def dowloadGame():
    url_game = "https://www.loveroms.com/download/super-nintendo/super-mario-world-u-/12720"
    game = g.Game("Super Mario World", url_game)
    game.run()


def boto():
    link = "https://download.loveroms.com/downloader/rom/12720/1/Super Mario World (U) [!].zip?token=1523630951-nG9Y%2F2Q12vj7gUIjFGlIKaZoQNkA3R0jLd7quAx1Dew%3D"
    r = req.requestURL()
    x = r.getFile(link)

    # print(x.CONTENT_DECODERS[0])
    print(x.headers['content-type'])
    bina = x.raw

    session = boto3.session.Session(
        aws_access_key_id="AKIAII35HUUWOECQFCGA",
        aws_secret_access_key="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"
    )
    s3 = session.resource('s3')
    bucket= s3.Bucket('rrom')

    file = 'Datas/SuperMarioWorld.zip'

    object_file = s3.Object('rrom', 'file_roms/nintendo/SuperMarioWorld3.zip')
    # vish = object_file.put(Body=open(file, 'rb'))
    vish = object_file.put(Body=bina.read())

    print(vish)

if __name__ == '__main__':
    all()