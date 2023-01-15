import devConfig from './dev';
import localKuberConfig from './localKuber';
import prodConfig from './prod';

const getConfig = () => {
    switch (process.env.DEPLOY) {
        case 'local-kuber':
            return localKuberConfig;
        case 'prod':
            return prodConfig;
        default:
            return devConfig;
    }
};

export default getConfig();
