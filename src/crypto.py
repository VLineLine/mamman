from os import getenv, path, mkdir
import rsa, base64

class tools(object):
    my_key_pub = None
    my_key_priv = None
    
    def __init__(self):
        (self.my_key_pub, self.my_key_priv) = self._get_keys()

    def _get_keys(self):
        path_user = getenv('LOCALAPPDATA')
        path_user = path.join(path_user, 'LTS AS')

        # Demand folder in localappdata
        if not path.exists(path_user):
            print('generating path in localappdata')
            mkdir(path_user)

        path_private_key = path.join(path_user, 'my_private_key.pem')
        path_public_key = path.join(path_user, 'my_public_key.pem')

        if not path.isfile(path_private_key):
            # Generate, register and save new keypair
            print('generating keypair')
            (my_key_pub, my_key_priv) = rsa.newkeys(2048)

            file = open(path_private_key,'wb')
            file.write(my_key_priv.save_pkcs1('PEM'))
            file.close()
            path_private_key = None

            file = open(path_public_key,'wb')
            file.write(my_key_pub.save_pkcs1('PEM'))
            file.close()
            path_public_key = None

            return (my_key_pub, my_key_priv)

        else:
            # Read existing keypair
            with open(path_private_key, mode='rb') as file:
                file_content = file.read()
            file.close()
            path_private_key = None
            my_key_priv = rsa.PrivateKey.load_pkcs1(file_content)
            file_content = None

            with open (path_public_key, 'rb') as file:
                file_content = file.read()
            file.close()
            path_public_key = None
            my_key_pub = rsa.PublicKey.load_pkcs1(file_content)
            file_content = None

            return (my_key_pub, my_key_priv)

    def get_credentials(self):
        return {
        'username': getenv('USERNAME'),
        'computername': getenv('COMPUTERNAME'),
        'userdomain': getenv('USERDOMAIN'),
        'key': self.my_key_pub.save_pkcs1('PEM').decode('ASCII'),
        }
    
      
if __name__ == '__main__':
    test = tools()
    print(test.get_credentials())
