# Vercel Deployment Guide

## 📦 Vercel Deployment Setup

Your Skill Swap Platform is now configured for Vercel deployment!

### 🚀 Quick Deploy Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy to Vercel**:
   ```bash
   vercel
   ```

### 🔧 Environment Variables

Set these environment variables in your Vercel dashboard:

#### Required Variables:
```bash
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://username:password@host:port/database
```

#### Optional (for Google OAuth):
```bash
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 🗄️ Database Setup

#### Option 1: Vercel Postgres (Recommended)
1. Go to your Vercel dashboard
2. Navigate to your project
3. Go to Storage tab
4. Create a new Postgres database
5. Copy the connection string to `DATABASE_URL`

#### Option 2: External PostgreSQL
- Use services like:
  - **Neon** (free tier available)
  - **PlanetScale** 
  - **Railway**
  - **Supabase**

### 📁 Project Structure for Vercel

```
your-project/
├── api/
│   └── index.py          # Main entry point for Vercel
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── models.py             # Database models
├── routes.py             # Main routes
├── config.py             # Configuration
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
├── runtime.txt          # Python version
└── .vercelignore        # Files to ignore during deployment
```

### 🔄 Deployment Commands

#### Deploy to production:
```bash
vercel --prod
```

#### Deploy preview:
```bash
vercel
```

#### Check deployment status:
```bash
vercel ls
```

### 🌐 Custom Domain

1. Go to your Vercel dashboard
2. Navigate to your project
3. Go to Settings → Domains
4. Add your custom domain

### 🐛 Troubleshooting

#### Common Issues:

1. **Database Connection Error**:
   - Ensure `DATABASE_URL` is set correctly
   - Check if database allows external connections

2. **Static Files Not Loading**:
   - Verify `static/` folder structure
   - Check CSS/JS file paths in templates

3. **Import Errors**:
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

4. **OAuth Redirect Issues**:
   - Update Google OAuth authorized redirect URIs
   - Add your Vercel domain to allowed origins

### 📊 Monitoring

- Check logs: `vercel logs`
- Monitor performance in Vercel dashboard
- Set up alerts for errors

### 🔒 Security Notes

- Never commit `.env` files
- Use strong secrets for production
- Enable HTTPS (automatic with Vercel)
- Configure CORS if needed

### 🚦 Production Checklist

- [ ] Environment variables set
- [ ] Database configured
- [ ] Google OAuth configured (if using)
- [ ] Static files loading correctly
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active
- [ ] Error monitoring setup

---

## 🎉 Your app will be live at:
`https://your-project-name.vercel.app`

### Support Resources:
- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [PostgreSQL on Vercel](https://vercel.com/docs/storage/vercel-postgres)
