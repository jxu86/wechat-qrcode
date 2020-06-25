from wxpy import *
# import redis
import argparse
import pytoml
import qrcode_server as qs

bot = Bot(console_qr=True, cache_path=True)

class Server():
    def __init__(self, params):
        self._config = params['config']
        self._receivers = []
        self._bot = bot
        self.get_receivers()

   # bot.groups().search('优选品牌限时超低折扣群')[0],
    @bot.register(chats = [bot.groups().search('优选品牌限时超低折扣群')[0]], except_self=False)
    # @bot.register(chats = [bot.groups().search('warnning')[0]], except_self=False)
    def monitorGroup(msg):
        # print('msg type==>',type(msg))
        print('msg type==>',msg.type)
        # print('msg member==>',msg.member)
        print('msg member name==>',msg.member.name)
        if msg.type == 'Picture' and msg.member.name == '晴朗':
            msg.get_file('file_tmp/tmp.jpg')
            try:
                filePath = qs.createNewImg('file_tmp/tmp.jpg')
                if filePath:
                    # g = bot.groups().search('warnning')[0] # 周小姐的品牌正品特卖店
                    g = bot.groups().search('周小姐的品牌正品特卖店')[0]
                    print('group==>', g)
                    g.send_image(filePath)
            except Exception as e:
                print('createNewImg error:{}'.format(e))
            # self.handle_data('tmp.jpg')
            
    
    def get_receivers(self):
        print('groups =>', self._bot.groups())
        # try:
        #     if 'friends' in self._config:
        #         self._receivers += [self._bot.friends().search(f)[0] for f in self._config['friends']]
        #     if 'groups' in self._config:
        #         self._receivers += [self._bot.groups().search(g)[0] for g in self._config['groups']]
        #     # print('friends len=>', len(self._bot.friends()))
        #     for group in self._bot.groups():
        #         print(group)
        #     print(self._bot.groups().search('warnning')[0])
        #     print('wechat receivers: {}'.format(self._receivers))
        # except Exception as e:
        #     print('error: {}'.format(e))

    def handle_data(self, data):
        for friend in self._receivers:
            friend.send_image('tmp.jpg')
        # for friend in self._receivers:
        #     friend.send(data)
        
    def run(self):
        print('run...')
        # self.handle_data('hello world!')
        self._bot.join()
        # while True:
        #     pass

def parse_config(config_path):
    with open(config_path) as f:
        config = pytoml.load(f)

    return config
    
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        default='config.toml',
        help='Config file (default: \'config.toml\')')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    print('##main##')
    args = parse_args()
    print('args: {}'.format(args))
    config = parse_config(args.config)
    print('config: {}',config)
    server = Server(config)
    server.run()