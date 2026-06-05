// middleware/apiKeyAuth.js
module.exports = function apiKeyAuth(req, res, next) {
  const adminKey = process.env.ADMIN_API_KEY;

  // If no ADMIN_API_KEY is set, skip auth (open API)
  if (!adminKey) {
    return next();
  }

  // Allow public GET endpoints
  const publicAllow = [
    '/api/v1/health',
    '/api/v1/models'
  ];
  if (req.method === 'GET' && publicAllow.includes(req.path)) {
    return next();
  }

  // Support X-API-KEY header or Authorization: Bearer <key>
  const headerKey = (req.headers['x-api-key'] || '').toString();
  const authHeader = (req.headers['authorization'] || '').toString();
  let bearer = '';
  if (authHeader.toLowerCase().startsWith('bearer ')) {
    bearer = authHeader.split(' ')[1];
  }

  const provided = headerKey || bearer;

  if (!provided) {
    return res.status(401).json({ error: 'Missing API key' });
  }

  if (provided !== adminKey) {
    return res.status(403).json({ error: 'Invalid API key' });
  }

  return next();
};
