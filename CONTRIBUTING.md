# Contributing to Claude Code Plugin Marketplace

Thank you for your interest in contributing to the Claude Code Plugin Marketplace! This guide will help you create and submit high-quality plugins.

## Table of Contents

- [Getting Started](#getting-started)
- [Plugin Requirements](#plugin-requirements)
- [Plugin Structure](#plugin-structure)
- [Development Guidelines](#development-guidelines)
- [Testing Requirements](#testing-requirements)
- [Submission Process](#submission-process)
- [Review Criteria](#review-criteria)

## Getting Started

### Prerequisites

- Node.js 16+ (if your plugin uses JavaScript)
- Claude Code CLI installed
- Git for version control
- Familiarity with Claude Code plugin architecture

### Fork and Clone

1. Fork this repository
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/marketplace.git
   cd marketplace
   ```

## Plugin Requirements

### Mandatory Requirements

All plugins MUST include:

1. **plugin.json** - Complete metadata file
2. **README.md** - Comprehensive documentation
3. **LICENSE** - Open source license file
4. **src/** - Source code directory
5. **tests/** - Test suite with >80% coverage
6. **examples/** - Usage examples

### plugin.json Structure

Your `plugin.json` must include these required fields:

```json
{
  "name": "your-plugin-name",
  "version": "1.0.0",
  "description": "Clear, concise description (max 200 chars)",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com",
    "url": "https://yourwebsite.com"
  },
  "main": "src/index.js",
  "claudeVersion": ">=1.0.0",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/your-username/your-plugin"
  }
}
```

### Optional Fields

```json
{
  "homepage": "https://your-plugin-docs.com",
  "bugs": {
    "url": "https://github.com/your-username/your-plugin/issues"
  },
  "dependencies": {
    "package-name": "^1.0.0"
  },
  "devDependencies": {
    "testing-package": "^2.0.0"
  },
  "scripts": {
    "test": "jest",
    "lint": "eslint src/"
  },
  "engines": {
    "node": ">=16.0.0"
  },
  "category": "development-tools",
  "tags": ["testing", "automation", "ci-cd"],
  "configuration": {
    "properties": {
      "apiKey": {
        "type": "string",
        "description": "API key for external service"
      }
    }
  }
}
```

## Plugin Structure

### Standard Directory Layout

```
plugins/your-plugin-name/
├── plugin.json              # Plugin metadata
├── README.md                # Main documentation
├── LICENSE                  # License file
├── CHANGELOG.md             # Version history
├── .gitignore              # Git ignore rules
├── src/                    # Source code
│   ├── index.js            # Main entry point
│   ├── agents/             # Agent definitions
│   │   └── specialized-agent.js
│   ├── tools/              # Custom tools
│   │   └── custom-tool.js
│   ├── utils/              # Utility functions
│   │   └── helpers.js
│   └── config/             # Configuration files
│       └── defaults.js
├── tests/                  # Test files
│   ├── unit/               # Unit tests
│   │   └── agents.test.js
│   ├── integration/        # Integration tests
│   │   └── workflow.test.js
│   └── fixtures/           # Test fixtures
│       └── sample-data.json
├── examples/               # Usage examples
│   ├── basic-usage.md
│   ├── advanced-usage.md
│   └── code-samples/
│       └── example.js
├── docs/                   # Additional documentation
│   ├── api.md
│   ├── configuration.md
│   └── troubleshooting.md
└── assets/                 # Images, diagrams, etc.
    └── architecture.png
```

## Development Guidelines

### Code Quality Standards

1. **Code Style**
   - Use consistent formatting (recommend Prettier)
   - Follow JavaScript/TypeScript best practices
   - Include JSDoc comments for public APIs
   - Keep functions small and focused

2. **Error Handling**
   - Validate all inputs
   - Provide clear error messages
   - Handle edge cases gracefully
   - Never expose sensitive information in errors

3. **Performance**
   - Optimize for common use cases
   - Avoid blocking operations
   - Implement caching where appropriate
   - Monitor memory usage

4. **Security**
   - Never hardcode credentials
   - Validate and sanitize all user inputs
   - Use secure dependencies (no known vulnerabilities)
   - Follow OWASP security guidelines

### Documentation Requirements

#### README.md Must Include:

1. **Plugin Overview**
   - What the plugin does
   - Key features
   - Use cases

2. **Installation**
   - Step-by-step installation instructions
   - Dependencies
   - Configuration requirements

3. **Usage**
   - Quick start example
   - Common use cases
   - Code examples

4. **API Reference**
   - Available commands/functions
   - Parameters and return values
   - Examples for each API

5. **Configuration**
   - Available configuration options
   - Default values
   - Configuration examples

6. **Troubleshooting**
   - Common issues and solutions
   - Debug tips
   - Where to get help

7. **Contributing**
   - How to contribute to the plugin
   - Development setup
   - Coding standards

8. **License**
   - License type
   - Copyright information

## Testing Requirements

### Minimum Coverage

- Unit test coverage: **>80%**
- Integration test coverage: **>70%**
- All critical paths must be tested

### Test Structure

```javascript
// tests/unit/agent.test.js
describe('SpecializedAgent', () => {
  describe('initialization', () => {
    it('should initialize with default configuration', () => {
      // Test implementation
    });

    it('should validate required parameters', () => {
      // Test implementation
    });
  });

  describe('execution', () => {
    it('should handle valid inputs correctly', () => {
      // Test implementation
    });

    it('should handle errors gracefully', () => {
      // Test implementation
    });
  });
});
```

### Testing Best Practices

1. Write tests before code (TDD approach recommended)
2. Test both success and failure scenarios
3. Use meaningful test descriptions
4. Mock external dependencies
5. Keep tests fast and isolated
6. Include integration tests for workflows
7. Test error conditions and edge cases

### Running Tests

Your plugin should support:

```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run linting
npm run lint

# Run integration tests
npm run test:integration
```

## Submission Process

### Step-by-Step Submission

1. **Prepare Your Plugin**
   ```bash
   # Create plugin directory
   mkdir -p plugins/your-plugin-name
   cd plugins/your-plugin-name

   # Initialize plugin structure
   # Add all required files
   ```

2. **Test Thoroughly**
   ```bash
   # Run all tests
   npm test

   # Verify linting
   npm run lint

   # Test in a real project
   claude plugin install ./plugins/your-plugin-name
   ```

3. **Create Documentation**
   - Write comprehensive README.md
   - Add usage examples
   - Document all configuration options
   - Include troubleshooting guide

4. **Commit Your Changes**
   ```bash
   git checkout -b add-your-plugin-name
   git add plugins/your-plugin-name
   git commit -m "Add your-plugin-name plugin"
   ```

5. **Push and Create PR**
   ```bash
   git push origin add-your-plugin-name
   ```

   Then create a Pull Request with:
   - Clear title: "Add [Plugin Name] plugin"
   - Description of what the plugin does
   - Testing evidence (screenshots, test results)
   - Breaking changes (if any)

### Pull Request Template

```markdown
## Plugin Submission: [Plugin Name]

### Description
Brief description of what this plugin does.

### Category
- [ ] Agent Coordination
- [ ] Development Tools
- [ ] Integration
- [ ] Analysis
- [ ] Documentation
- [ ] Other: ___________

### Checklist
- [ ] plugin.json includes all required fields
- [ ] README.md with comprehensive documentation
- [ ] LICENSE file included
- [ ] Tests included (>80% coverage)
- [ ] Examples directory with usage examples
- [ ] All tests passing
- [ ] No security vulnerabilities
- [ ] Follows coding standards

### Testing Evidence
Describe how you tested the plugin and paste test results.

### Additional Notes
Any additional information reviewers should know.
```

## Review Criteria

### What Reviewers Look For

1. **Functionality**
   - Plugin works as described
   - Solves a real problem
   - Adds value to Claude Code ecosystem

2. **Code Quality**
   - Clean, readable code
   - Follows best practices
   - Well-documented
   - Properly structured

3. **Testing**
   - Comprehensive test coverage
   - Tests are meaningful
   - All tests pass

4. **Documentation**
   - Clear and complete
   - Examples are helpful
   - Easy to follow

5. **Security**
   - No security vulnerabilities
   - Safe handling of user data
   - Secure dependency usage

6. **Performance**
   - Efficient implementation
   - No obvious bottlenecks
   - Resource usage is reasonable

### Review Timeline

- Initial review: **3-5 business days**
- Revisions: **2-3 business days** per iteration
- Final approval: **1-2 business days**

### Feedback and Iterations

- Reviewers may request changes
- Address feedback promptly
- Push updates to the same PR
- Engage constructively with reviewers

## Support and Questions

- **Questions**: Open a GitHub Discussion
- **Issues**: Report in GitHub Issues
- **Chat**: Join our Discord community
- **Email**: marketplace@claude-code.dev

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on improving the ecosystem
- Help other contributors

## License

By contributing, you agree that your contributions will be licensed under the same license as the plugin you're contributing to (typically MIT).

---

Thank you for contributing to the Claude Code Plugin Marketplace! Your plugins help make development better for everyone.
