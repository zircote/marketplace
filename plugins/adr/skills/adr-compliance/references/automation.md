# ADR Compliance Automation

Strategies and tools for automating ADR compliance checking.

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: ADR Compliance

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  adr-compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Load ADR Configuration
        id: adr-config
        run: |
          if [ -f ".claude/adr.local.md" ]; then
            echo "config_exists=true" >> $GITHUB_OUTPUT
          fi

      - name: Check Technology Compliance
        run: |
          echo "Checking database technology..."
          if grep -rq "mysql\|mongodb" src/; then
            echo "::error::Non-approved database technology found"
            exit 1
          fi

      - name: Check Architecture Patterns
        run: |
          echo "Checking for direct service calls..."
          # Add pattern checks based on your ADRs

      - name: Generate Compliance Report
        if: always()
        run: |
          echo "## ADR Compliance Report" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Check | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|-------|--------|" >> $GITHUB_STEP_SUMMARY
```

### GitLab CI Pipeline

```yaml
stages:
  - lint
  - test
  - compliance

adr-compliance:
  stage: compliance
  script:
    - ./scripts/adr-compliance-check.sh
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  artifacts:
    reports:
      junit: compliance-report.xml
    paths:
      - compliance-report.md
    when: always
```

### Azure DevOps Pipeline

```yaml
trigger:
  branches:
    include:
      - main
      - develop

stages:
  - stage: Compliance
    jobs:
      - job: ADRCompliance
        steps:
          - script: |
              ./scripts/adr-compliance-check.sh
            displayName: 'Check ADR Compliance'
          - task: PublishTestResults@2
            inputs:
              testResultsFormat: 'JUnit'
              testResultsFiles: '**/compliance-*.xml'
```

## Architecture Testing Tools

### ArchUnit (Java/Kotlin)

```java
import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;

public class ADRComplianceTest {

    private final JavaClasses classes = new ClassFileImporter()
        .importPackages("com.example");

    // ADR-001: Controllers must use services, not repositories
    @Test
    void controllersShouldNotAccessRepositories() {
        ArchRule rule = noClasses()
            .that().resideInAPackage("..controller..")
            .should().accessClassesThat()
            .resideInAPackage("..repository..");

        rule.check(classes);
    }

    // ADR-002: Domain layer should not depend on infrastructure
    @Test
    void domainShouldNotDependOnInfrastructure() {
        ArchRule rule = noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAPackage("..infrastructure..");

        rule.check(classes);
    }

    // ADR-003: All REST endpoints must have security annotations
    @Test
    void endpointsMustBeSecured() {
        ArchRule rule = methods()
            .that().areAnnotatedWith(GetMapping.class)
            .or().areAnnotatedWith(PostMapping.class)
            .should().beAnnotatedWith(PreAuthorize.class);

        rule.check(classes);
    }
}
```

### Dependency-Cruiser (JavaScript/TypeScript)

```javascript
// .dependency-cruiser.js
module.exports = {
  forbidden: [
    // ADR-001: UI should not import from data layer
    {
      name: 'no-ui-to-data',
      severity: 'error',
      from: { path: '^src/ui' },
      to: { path: '^src/data' }
    },
    // ADR-002: Services should not import from controllers
    {
      name: 'no-service-to-controller',
      severity: 'error',
      from: { path: '^src/services' },
      to: { path: '^src/controllers' }
    },
    // ADR-003: No direct database imports outside data layer
    {
      name: 'database-only-in-data',
      severity: 'error',
      from: { pathNot: '^src/data' },
      to: { path: 'node_modules/(pg|mysql|mongodb)' }
    }
  ],
  options: {
    doNotFollow: {
      path: 'node_modules'
    }
  }
};
```

### ESLint Custom Rules

```javascript
// eslint-rules/no-direct-service-calls.js
module.exports = {
  meta: {
    type: 'problem',
    docs: {
      description: 'ADR-005: Disallow direct service-to-service HTTP calls',
    },
  },
  create(context) {
    return {
      ImportDeclaration(node) {
        if (node.source.value.includes('axios') ||
            node.source.value.includes('node-fetch')) {
          if (context.getFilename().includes('/services/')) {
            context.report({
              node,
              message: 'ADR-005 Violation: Services should use event bus, not direct HTTP calls'
            });
          }
        }
      }
    };
  }
};
```

## Pre-commit Hooks

### Husky + lint-staged

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged && npm run adr:check"
    }
  },
  "lint-staged": {
    "src/**/*.ts": [
      "npm run adr:check:staged"
    ]
  },
  "scripts": {
    "adr:check": "./scripts/adr-compliance.sh",
    "adr:check:staged": "./scripts/adr-compliance-staged.sh"
  }
}
```

### Pre-commit Framework (Python)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: adr-compliance
        name: ADR Compliance Check
        entry: ./scripts/adr-compliance.sh
        language: script
        files: \.(py|ts|js|java)$
        stages: [commit]
```

## Scheduled Audits

### Cron-based Full Audit

```yaml
# GitHub Actions scheduled workflow
name: Weekly ADR Audit

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
  workflow_dispatch:

jobs:
  full-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Full ADR Audit
        run: ./scripts/full-adr-audit.sh

      - name: Create Issue on Violations
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'ADR Compliance Violations Detected',
              body: 'Weekly audit found compliance issues. See workflow run for details.',
              labels: ['adr', 'compliance', 'automated']
            })
```

## Monitoring and Alerting

### Compliance Metrics

```bash
#!/bin/bash
# collect-compliance-metrics.sh

# Count violations by ADR
echo "compliance_violations{adr=\"001\"} $(grep -rc 'mysql' src/ | grep -v ':0$' | wc -l)"
echo "compliance_violations{adr=\"002\"} $(grep -rc 'direct.*call' src/services/ | wc -l)"

# Track over time
DATE=$(date +%Y-%m-%d)
echo "$DATE,ADR-001,$(grep -rc 'mysql' src/ | wc -l)" >> metrics/compliance-history.csv
```

### Slack/Teams Notifications

```bash
#!/bin/bash
# notify-violations.sh

VIOLATIONS=$(./scripts/adr-compliance.sh 2>&1)
VIOLATION_COUNT=$(echo "$VIOLATIONS" | grep -c "VIOLATION")

if [ $VIOLATION_COUNT -gt 0 ]; then
  curl -X POST "$SLACK_WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -d "{
      \"text\": \"ADR Compliance Alert: $VIOLATION_COUNT violations found\",
      \"blocks\": [{
        \"type\": \"section\",
        \"text\": {
          \"type\": \"mrkdwn\",
          \"text\": \"*ADR Compliance Report*\n$VIOLATIONS\"
        }
      }]
    }"
fi
```

## Compliance Dashboard

### Generate HTML Report

```bash
#!/bin/bash
# generate-dashboard.sh

cat > compliance-dashboard.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <title>ADR Compliance Dashboard</title>
  <style>
    .compliant { color: green; }
    .violation { color: red; }
    .warning { color: orange; }
  </style>
</head>
<body>
  <h1>ADR Compliance Dashboard</h1>
  <table>
    <tr><th>ADR</th><th>Status</th><th>Violations</th></tr>
EOF

# Add rows for each ADR
for adr in docs/adr/[0-9]*.md; do
  ID=$(basename "$adr" | cut -d'-' -f1)
  # Check compliance and add row
done

echo "</table></body></html>" >> compliance-dashboard.html
```

## Best Practices

### Gradual Enforcement

1. **Phase 1**: Warning only (collect data)
2. **Phase 2**: Block new violations
3. **Phase 3**: Require remediation of existing violations

### Exemption Process

```yaml
# .adr-compliance-ignore
# Format: file_pattern:ADR_ID:reason:expiry_date
src/legacy/*:ADR-001:Legacy code pending migration:2024-06-01
src/migrations/*:ADR-002:Migration scripts exempt:permanent
```

### Documentation Integration

Link compliance checks back to ADRs:
```markdown
## ADR-001: Use PostgreSQL

### Compliance

**Automated Checks**:
- CI pipeline: `adr-compliance.yml`
- Pre-commit hook: `check-database-imports`

**Manual Review Required For**:
- New database dependencies in package.json
- Changes to database configuration
```
