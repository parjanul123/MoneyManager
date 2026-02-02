DELETE FROM socialaccount_socialapp WHERE provider='discord';
DELETE FROM socialaccount_socialapp_sites WHERE socialapp_id IN (SELECT id FROM socialaccount_socialapp WHERE provider='discord');
