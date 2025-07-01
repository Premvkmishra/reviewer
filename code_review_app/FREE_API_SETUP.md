# 🆓 Free API Setup Guide for Code Analysis

This guide will help you set up free APIs for AI-powered code analysis without any local storage requirements.

## 🎯 Quick Start (Choose One)

### Option 1: Hugging Face (Recommended - Completely Free)
**✅ 30,000 requests per month FREE**

1. **Sign up**: Go to [Hugging Face](https://huggingface.co/join)
2. **Get token**: 
   - Go to [Settings → Access Tokens](https://huggingface.co/settings/tokens)
   - Click "New token"
   - Name: "Code Review App"
   - Role: "Read"
   - Click "Generate token"
3. **Copy token** and add to your `.env` file:
   ```
   HF_API_TOKEN=hf_your_token_here
   ```

### Option 2: OpenAI (Free $5 Credit)
**✅ $5 free credit (about 1000-2000 requests)**

1. **Sign up**: Go to [OpenAI Platform](https://platform.openai.com/signup)
2. **Get API key**:
   - Go to [API Keys](https://platform.openai.com/api-keys)
   - Click "Create new secret key"
   - Copy the key
3. **Add to `.env`**:
   ```
   OPENAI_API_KEY=sk-your_key_here
   ```

### Option 3: Anthropic Claude (Free Tier)
**✅ Limited free requests per day**

1. **Sign up**: Go to [Anthropic Console](https://console.anthropic.com/)
2. **Get API key**:
   - Click "Get API Key"
   - Copy the key
3. **Add to `.env`**:
   ```
   ANTHROPIC_API_KEY=sk-ant-your_key_here
   ```

## 🚀 Setup Steps

### 1. Copy Environment File
```bash
cp env_example.txt .env
```

### 2. Edit .env File
Add your chosen API key to the `.env` file:
```bash
# For Hugging Face (recommended)
HF_API_TOKEN=hf_your_token_here

# OR for OpenAI
OPENAI_API_KEY=sk-your_key_here

# OR for Anthropic
ANTHROPIC_API_KEY=sk-ant-your_key_here
```

### 3. Start the Backend
```bash
python start.py
```

### 4. Test the API
Visit: `http://localhost:8000/docs`

## 📊 API Comparison

| Service | Free Tier | Best For | Setup Difficulty |
|---------|-----------|----------|------------------|
| **Hugging Face** | 30K requests/month | General use | ⭐ Easy |
| **OpenAI** | $5 credit | High quality | ⭐⭐ Medium |
| **Anthropic** | Limited/day | Code analysis | ⭐⭐ Medium |

## 🔧 How It Works

The app automatically tries APIs in this order:
1. **Hugging Face** (if token provided)
2. **OpenAI** (if key provided) 
3. **Anthropic** (if key provided)
4. **Fallback** (rule-based analysis - always works)

## 💡 Tips

- **Start with Hugging Face** - it's completely free and easy to set up
- **You only need ONE API key** to get started
- **The fallback analysis always works** even without any API keys
- **All APIs are cloud-based** - no local storage needed

## 🆘 Troubleshooting

### "Invalid API token" error
- Check that your token/key is copied correctly
- Ensure there are no extra spaces
- Verify the token has the right permissions

### "Rate limit exceeded" error
- Hugging Face: Wait a few minutes or upgrade plan
- OpenAI: Your $5 credit is used up
- Anthropic: Daily limit reached

### "Model loading" error
- This is normal for Hugging Face models
- Wait 30-60 seconds and try again
- The app will automatically retry

## 🎉 Success!

Once you have any API key set up, your code analysis will be much more comprehensive and accurate than the basic rule-based fallback.

**Remember**: The app works even without any API keys - it will use the enhanced rule-based analysis as a fallback. 