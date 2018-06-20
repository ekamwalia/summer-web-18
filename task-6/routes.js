const router = require('express').Router()
const controller = require('./controller');

// TODO: Autogenerate routes

router.get('/', (req, res) => res.redirect('/login'));

router.get('/register', controller.GET_register);
router.post('/register', controller.POST_register);

router.get('/login', controller.GET_login);
router.post('/login', controller.POST_login);

router.get('/profile', controller.GET_profile);

router.post('/search', controller.POST_search);
router.post('/star', controller.POST_star);

router.get('/user/:owner', controller.GET_user);

router.get('/user/:owner/:repo', controller.GET_repo);

router.get('/user/:owner/:repo/*', controller.GET_repoContents);

router.post('/logout', controller.POST_logout);

router.get('/boilerplate', controller.GET_boilerplate);

module.exports = router;