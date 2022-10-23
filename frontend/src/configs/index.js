import devConfig from './dev';
import localKuberConfig from './localKuber';

export default process.env.DEPLOY === 'local-kuber' ? localKuberConfig : devConfig;
