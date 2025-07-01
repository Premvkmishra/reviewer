import os
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

# Free Hugging Face API - 30,000 requests/month free
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "hf_abc123DUMMYtoken")

# Free model options - no local storage needed
FREE_MODELS = {
    "code_analysis": "microsoft/DialoGPT-medium",  # Free, good for text generation
    "code_quality": "gpt2",  # Free, basic text generation
    "fallback": "distilgpt2"  # Free, lightweight
}

# Alternative free APIs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Free $5 credit
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")  # Free tier

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def analyze_code(code: str, language: str | None) -> str:
    """Analyze code using free APIs in order of preference"""
    
    # Try Hugging Face first (free tier)
    try:
        return await analyze_with_huggingface(code, language)
    except Exception as e:
        print(f"Hugging Face failed: {e}")
    
    # Try OpenAI if available (free $5 credit)
    if OPENAI_API_KEY and OPENAI_API_KEY != "":
        try:
            return await analyze_with_openai(code, language)
        except Exception as e:
            print(f"OpenAI failed: {e}")
    
    # Try Anthropic if available (free tier)
    if ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "":
        try:
            return await analyze_with_anthropic(code, language)
        except Exception as e:
            print(f"Anthropic failed: {e}")
    
    # Fallback to rule-based analysis
    return fallback_analysis(code, language)

async def analyze_with_huggingface(code: str, language: str | None) -> str:
    """Use Hugging Face free inference API"""
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        
        # Create a structured prompt for better analysis
        prompt = f"""Analyze this {language or 'code'} for bugs, security issues, and improvements:

```{language or 'text'}
{code}
```

Provide analysis in markdown format with sections for:
1. Security Vulnerabilities
2. Bugs and Issues  
3. Code Quality Suggestions
4. Best Practices

Be concise but thorough."""

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 800,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        # Try different free models
        for model_name in FREE_MODELS.values():
            try:
                response = await client.post(
                    f"https://api-inference.huggingface.co/models/{model_name}",
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Handle different response formats
                    if isinstance(result, list) and len(result) > 0:
                        if "generated_text" in result[0]:
                            return result[0]["generated_text"]
                        elif "text" in result[0]:
                            return result[0]["text"]
                    elif isinstance(result, dict):
                        if "generated_text" in result:
                            return result["generated_text"]
                        elif "text" in result:
                            return result["text"]
                    
                    return str(result)
                elif response.status_code == 503:
                    # Model is loading, try next one
                    continue
                    
            except Exception:
                continue
        
        raise Exception("All Hugging Face models are currently unavailable")

async def analyze_with_openai(code: str, language: str | None) -> str:
    """Use OpenAI API (free $5 credit)"""
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Analyze this {language or 'code'} for bugs, security vulnerabilities, and code quality issues:

```{language or 'text'}
{code}
```

Provide a detailed analysis in markdown format covering:
1. **Security Vulnerabilities**: Any security issues found
2. **Bugs**: Logic errors or potential runtime issues  
3. **Code Quality**: Suggestions for improvement
4. **Best Practices**: Recommendations for better coding

Be specific and actionable."""

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an expert code reviewer and security analyst."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.3
        }
        
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"OpenAI API error: {response.status_code}")

async def analyze_with_anthropic(code: str, language: str | None) -> str:
    """Use Anthropic Claude API (free tier)"""
    async with httpx.AsyncClient() as client:
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        prompt = f"""Analyze this {language or 'code'} for bugs, security vulnerabilities, and code quality issues:

```{language or 'text'}
{code}
```

Provide a detailed analysis in markdown format covering:
1. **Security Vulnerabilities**: Any security issues found
2. **Bugs**: Logic errors or potential runtime issues  
3. **Code Quality**: Suggestions for improvement
4. **Best Practices**: Recommendations for better coding

Be specific and actionable."""

        payload = {
            "model": "claude-instant-1.2",
            "max_tokens": 1000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["content"][0]["text"]
        else:
            raise Exception(f"Anthropic API error: {response.status_code}")

# Enhanced fallback analysis function
def fallback_analysis(code: str, language: str | None) -> str:
    """Comprehensive rule-based analysis as fallback"""
    issues = []
    warnings = []
    suggestions = []
    
    # Security vulnerability patterns
    security_patterns = [
        ("eval(", "🚨 **CRITICAL**: Use of eval() is extremely dangerous - allows arbitrary code execution"),
        ("exec(", "🚨 **CRITICAL**: Use of exec() is extremely dangerous - allows arbitrary code execution"),
        ("subprocess.call", "⚠️ **Security**: Be careful with subprocess calls - validate all inputs"),
        ("os.system", "⚠️ **Security**: os.system() is dangerous - use subprocess with proper arguments"),
        ("input(", "⚠️ **Security**: Validate user input to prevent injection attacks"),
        ("raw_input(", "⚠️ **Security**: Validate user input to prevent injection attacks"),
        ("document.write", "⚠️ **Security**: Avoid document.write() - can lead to XSS attacks"),
        ("innerHTML", "⚠️ **Security**: Be careful with innerHTML - validate content to prevent XSS"),
        ("innerText", "⚠️ **Security**: Be careful with innerText - validate content"),
        ("localStorage", "⚠️ **Security**: Don't store sensitive data in localStorage"),
        ("sessionStorage", "⚠️ **Security**: Don't store sensitive data in sessionStorage"),
        ("password", "🔒 **Security**: Ensure passwords are properly hashed and not logged"),
        ("secret", "🔒 **Security**: Check for hardcoded secrets or API keys"),
        ("api_key", "🔒 **Security**: Check for hardcoded API keys"),
        ("token", "🔒 **Security**: Check for hardcoded tokens"),
    ]
    
    # Code quality patterns
    quality_patterns = [
        ("TODO", "📝 **Code Quality**: TODO comment found - implement or remove"),
        ("FIXME", "🔧 **Code Quality**: FIXME comment found - fix the issue"),
        ("HACK", "🔧 **Code Quality**: HACK comment found - refactor this code"),
        ("console.log", "🧹 **Code Quality**: Remove console.log statements in production"),
        ("print(", "🧹 **Code Quality**: Remove print statements in production"),
        ("debugger", "🧹 **Code Quality**: Remove debugger statements in production"),
    ]
    
    # Performance patterns
    performance_patterns = [
        ("for i in range", "⚡ **Performance**: Consider using list comprehension or generator"),
        ("while True", "⚡ **Performance**: Ensure while True loops have proper exit conditions"),
        ("sleep(", "⚡ **Performance**: Avoid sleep() in production code"),
        ("time.sleep", "⚡ **Performance**: Avoid time.sleep() in production code"),
    ]
    
    # Check for patterns
    for pattern, message in security_patterns:
        if pattern in code:
            issues.append(message)
    
    for pattern, message in quality_patterns:
        if pattern in code:
            warnings.append(message)
    
    for pattern, message in performance_patterns:
        if pattern in code:
            suggestions.append(message)
    
    # Basic code structure analysis
    lines = code.split('\n')
    if len(lines) > 100:
        warnings.append("📏 **Code Quality**: Consider breaking this into smaller functions (over 100 lines)")
    
    if code.count('if') > code.count('else') * 2:
        warnings.append("🔍 **Code Quality**: Consider adding else clauses for better error handling")
    
    if code.count('try') > code.count('except') * 2:
        warnings.append("🛡️ **Code Quality**: Ensure all try blocks have proper except handlers")
    
    # Language-specific checks
    if language and language.lower() == 'python':
        if 'import *' in code:
            warnings.append("🐍 **Python**: Avoid 'import *' - import specific modules")
        if '__init__' in code and 'self.' not in code:
            warnings.append("🐍 **Python**: Check if __init__ method properly initializes instance variables")
    
    elif language and language.lower() in ['javascript', 'typescript']:
        if 'var ' in code:
            warnings.append("🟨 **JavaScript**: Use 'const' or 'let' instead of 'var'")
        if '===' not in code and '==' in code:
            warnings.append("🟨 **JavaScript**: Use strict equality (===) instead of loose equality (==)")
    
    # Generate report
    report = []
    
    if issues:
        report.append("## 🚨 Security Issues")
        report.extend(issues)
        report.append("")
    
    if warnings:
        report.append("## ⚠️ Code Quality Issues")
        report.extend(warnings)
        report.append("")
    
    if suggestions:
        report.append("## 💡 Suggestions")
        report.extend(suggestions)
        report.append("")
    
    if not issues and not warnings and not suggestions:
        report.append("## ✅ Analysis Complete")
        report.append("No obvious issues found in this code!")
        report.append("")
        report.append("**Note**: This is a basic rule-based analysis. For comprehensive review, consider:")
        report.append("- Setting up a Hugging Face API token for AI-powered analysis")
        report.append("- Using OpenAI API (free $5 credit) for detailed code review")
        report.append("- Running static analysis tools like ESLint, Pylint, or SonarQube")
    
    report.append("---")
    report.append(f"**Analysis Info**:")
    report.append(f"- Language: {language or 'Auto-detected'}")
    report.append(f"- Code Length: {len(code)} characters")
    report.append(f"- Lines: {len(lines)}")
    
    return "\n".join(report) 