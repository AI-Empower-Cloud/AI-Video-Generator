# GitHub Secrets Setup for AI Video Generator

This guide helps you set up GitHub repository secrets for the **AI-Empower-Cloud/AI-Video-Generator** repository.

## Required GitHub Secrets

You need to add the following secrets to your GitHub repository for Wasabi integration and CI/CD.

### 1. Access Your Repository Settings
1. Go to your GitHub repository: `https://github.com/AI-Empower-Cloud/AI-Video-Generator`
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

### 2. Add These Secrets One by One

#### WASABI_ACCESS_KEY
- Name: `WASABI_ACCESS_KEY`
- Value: Your Wasabi access key (from .env.wasabi file)

#### WASABI_SECRET_KEY
- Name: `WASABI_SECRET_KEY`
- Value: Your Wasabi secret key (from .env.wasabi file)

#### WASABI_BUCKET
- Name: `WASABI_BUCKET`
- Value: `ai-video-generator-content` (or your custom bucket name)

#### WASABI_REGION (Optional)
- Name: `WASABI_REGION`
- Value: `us-east-1` (default region)

#### WASABI_ENDPOINT (Optional)
- Name: `WASABI_ENDPOINT`
- Value: `https://s3.wasabisys.com` (default endpoint)

#### CDN_DOMAIN (Optional)
- Name: `CDN_DOMAIN`
- Value: Your CDN domain if you set one up (e.g., `https://cdn.empowerhub360.ai`)

## How to Get Your Wasabi Keys

### From .env.wasabi File
```bash
# View your current keys
cat /workspaces/AI-Video-Generator/.env.wasabi
```

### From Wasabi Console
1. Login to your Wasabi account
2. Go to **Access Keys** in the account menu
3. Find your key pair or create a new one
4. Copy the Access Key and Secret Key

## Testing the Setup

After adding the secrets, you can test the deployment by:

1. **Manual Trigger**: Go to Actions tab → Deploy to Wasabi → Run workflow
2. **Push Code**: Make any commit and push to main/master branch
3. **Create Tag**: Create a version tag (e.g., `git tag v1.0.1 && git push --tags`)

## Workflow Triggers

The deployment workflow runs automatically on:
- ✅ Push to `main` or `master` branch
- ✅ Push of version tags (e.g., `v1.0.0`, `v2.1.3`)
- ✅ Pull requests (for testing)
- ✅ Manual trigger from GitHub Actions tab

## Security Notes

🔒 **IMPORTANT**: Never commit sensitive keys to your repository!
- ✅ Keys are stored securely in GitHub Secrets
- ✅ Keys are only accessible during workflow execution
- ✅ Keys are automatically masked in logs
- ❌ Never put keys directly in workflow files

## Troubleshooting

### Common Issues:

1. **Invalid credentials**: Check that your keys are correct and active
2. **Permission denied**: Ensure your Wasabi keys have proper permissions
3. **Bucket not found**: Verify bucket name and region
4. **Network timeout**: Wasabi might be experiencing issues

### Debug Steps:

1. Check the workflow logs in GitHub Actions
2. Verify secrets are set correctly
3. Test credentials locally first:
   ```bash
   python3 test_wasabi_deployment.py
   ```

## What Happens During Deployment

1. 🧪 **Test Connection**: Verify Wasabi credentials work
2. 🎬 **Generate Content**: Create missing videos/audio if needed
3. 🚀 **Deploy Files**: Upload all content to Wasabi bucket
4. 🔧 **Configure Permissions**: Set bucket policy, CORS, and tags
5. 📊 **Create Report**: Generate deployment manifest and summary
6. 💬 **Notify Results**: Comment on PRs with deployment status

## Cost Estimate

With Wasabi's pricing:
- **Storage**: $0.0039/GB/month
- **Bandwidth**: FREE egress (downloads)
- **API calls**: Minimal cost

For a typical educational platform (~10GB content):
- **Monthly cost**: ~$0.04 (practically free!)
- **Annual cost**: ~$0.50

## Next Steps After Setup

1. ✅ Add all required secrets to GitHub
2. ✅ Test workflow by pushing a commit
3. ✅ Verify content is deployed to Wasabi
4. ✅ Set up your domain/CDN (optional)
5. ✅ Integrate with your Wix Studio site

---

**Need Help?** 
- Check the workflow logs in GitHub Actions
- Review this guide: `GITHUB_SECRETS_SETUP.md`
- Test locally with: `test_wasabi_deployment.py`
