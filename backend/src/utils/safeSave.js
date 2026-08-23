const { getConnectionStatus } = require('../config/db');

const safeSave = (savePromise) => {
  if (!getConnectionStatus()) return;
  if (savePromise && typeof savePromise.catch === 'function') {
    savePromise.catch((err) => {
      const msg = err?.message || '';
      if (
        msg.includes('bufferCommands') ||
        msg.includes('buffering') ||
        msg.includes('before initial connection') ||
        msg.includes('ECONNREFUSED')
      ) return;
      console.error('[DB Save Error]', msg);
    });
  }
};

module.exports = safeSave;
