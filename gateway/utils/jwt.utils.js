/**
 * 🔑 JWT Utils - Utility per Token
 */

const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'myzubster_secret_key_2026';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '24h';

// Genera token
exports.generateToken = (payload, expiresIn = JWT_EXPIRES_IN) => {
    return jwt.sign(payload, JWT_SECRET, { expiresIn });
};

// Verifica token
exports.verifyToken = (token) => {
    try {
        return jwt.verify(token, JWT_SECRET);
    } catch (error) {
        return null;
    }
};

// Decodifica token senza verifica
exports.decodeToken = (token) => {
    return jwt.decode(token);
};
