# Deployment: Enabling HTTPS with Nginx/Apache

## Nginx Example

1. **Obtain SSL Certificates**
   - Use Let's Encrypt or your CA to get `fullchain.pem` and `privkey.pem`.
   - Place them in `/etc/ssl/certs/` and `/etc/ssl/private/` (or your preferred secure location).

2. **Nginx Server Block**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/ssl/certs/fullchain.pem;
    ssl_certificate_key /etc/ssl/private/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Apache Example

1. **Obtain SSL Certificates**
   - Use Let's Encrypt or your CA to get `cert.pem` and `privkey.pem`.
   - Place them in `/etc/ssl/certs/` and `/etc/ssl/private/`.

2. **Apache VirtualHost**
```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com

    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/cert.pem
    SSLCertificateKeyFile /etc/ssl/private/privkey.pem

    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```

**Note:**
- Replace `yourdomain.com` with your actual domain.
- Ensure your firewall allows HTTPS (port 443).
- Restart Nginx/Apache after making changes.
