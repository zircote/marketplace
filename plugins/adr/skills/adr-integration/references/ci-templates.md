# CI/CD Pipeline Templates for ADRs

Ready-to-use pipeline configurations for ADR validation and automation.

## GitHub Actions

### Basic ADR Validation

```yaml
# .github/workflows/adr-validation.yml
name: ADR Validation

on:
  pull_request:
    paths:
      - 'docs/adr/**'
      - '.claude/adr.local.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate ADR Format
        run: |
          for file in docs/adr/[0-9]*.md; do
            echo "Validating $file..."

            # Check for required sections
            if ! grep -q "^## Status" "$file"; then
              echo "::error file=$file::Missing Status section"
              exit 1
            fi

            if ! grep -q "^## Context" "$file" && ! grep -q "^## Context and Problem Statement" "$file"; then
              echo "::error file=$file::Missing Context section"
              exit 1
            fi

            if ! grep -q "^## Decision" "$file" && ! grep -q "^## Decision Outcome" "$file"; then
              echo "::error file=$file::Missing Decision section"
              exit 1
            fi
          done
          echo "All ADRs validated successfully"

      - name: Check ADR Numbering
        run: |
          LAST_NUM=0
          for file in docs/adr/[0-9]*.md; do
            NUM=$(basename "$file" | grep -oE '^[0-9]+')
            NUM=$((10#$NUM))  # Remove leading zeros
            if [ $NUM -le $LAST_NUM ]; then
              echo "::error::ADR numbering issue: $file"
            fi
            LAST_NUM=$NUM
          done

      - name: Validate Links
        run: |
          for file in docs/adr/[0-9]*.md; do
            # Check for broken internal links
            grep -oE '\[ADR-[0-9]+\]\(\./[^)]+\)' "$file" | while read link; do
              TARGET=$(echo "$link" | grep -oE '\./[^)]+')
              if [ ! -f "docs/adr/$TARGET" ]; then
                echo "::warning file=$file::Broken link: $link"
              fi
            done
          done
```

### ADR Index Generation

```yaml
# .github/workflows/adr-index.yml
name: Update ADR Index

on:
  push:
    branches: [main]
    paths:
      - 'docs/adr/[0-9]*.md'

jobs:
  update-index:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - name: Generate ADR Index
        run: |
          cat > docs/adr/README.md << 'HEADER'
          # Architecture Decision Records

          This directory contains Architecture Decision Records (ADRs) for this project.

          ## ADR Index

          | ID | Title | Status | Date |
          |----|-------|--------|------|
          HEADER

          for file in docs/adr/[0-9]*.md; do
            ID=$(basename "$file" | grep -oE '^[0-9]+')
            TITLE=$(grep -m1 "^# " "$file" | sed 's/^# //')
            STATUS=$(grep -A1 "^## Status" "$file" | tail -1 | tr -d '\n\r')
            DATE=$(stat -c %y "$file" 2>/dev/null || stat -f %Sm "$file" | cut -d' ' -f1)

            echo "| $ID | [$TITLE](./$file) | $STATUS | $DATE |" >> docs/adr/README.md
          done

      - name: Commit Changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/adr/README.md
          git diff --staged --quiet || git commit -m "docs(adr): update ADR index [skip ci]"
          git push
```

### Full ADR Workflow

```yaml
# .github/workflows/adr-full.yml
name: ADR Workflow

on:
  pull_request:
    paths:
      - 'docs/adr/**'
  push:
    branches: [main]
    paths:
      - 'docs/adr/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate ADR Format
        run: ./scripts/validate-adrs.sh

      - name: Check for Duplicate Numbers
        run: |
          NUMS=$(ls docs/adr/[0-9]*.md | xargs -n1 basename | grep -oE '^[0-9]+' | sort)
          UNIQUE=$(echo "$NUMS" | uniq)
          if [ "$NUMS" != "$UNIQUE" ]; then
            echo "::error::Duplicate ADR numbers found"
            exit 1
          fi

  compliance:
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4

      - name: Check Code Compliance
        run: ./scripts/adr-compliance.sh

  update-index:
    runs-on: ubuntu-latest
    needs: [validate, compliance]
    if: github.ref == 'refs/heads/main'
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - name: Generate Index
        run: ./scripts/generate-adr-index.sh
      - name: Commit
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/adr/README.md
          git diff --staged --quiet || git commit -m "docs(adr): update index [skip ci]"
          git push
```

## GitLab CI

### Basic Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - compliance
  - publish

variables:
  ADR_PATH: docs/adr

adr-validate:
  stage: validate
  rules:
    - changes:
        - docs/adr/**
  script:
    - |
      for file in $ADR_PATH/[0-9]*.md; do
        echo "Validating $file"
        grep -q "^## Status" "$file" || (echo "Missing Status in $file" && exit 1)
        grep -q "^## Context" "$file" || grep -q "^## Context and Problem Statement" "$file" || (echo "Missing Context in $file" && exit 1)
      done

adr-compliance:
  stage: compliance
  rules:
    - changes:
        - src/**
  script:
    - ./scripts/adr-compliance.sh
  allow_failure: true

adr-publish:
  stage: publish
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      changes:
        - docs/adr/**
  script:
    - ./scripts/generate-adr-index.sh
  artifacts:
    paths:
      - docs/adr/README.md
```

### With Pages Deployment

```yaml
# GitLab CI with Pages
pages:
  stage: deploy
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  script:
    - mkdir -p public
    - ./scripts/export-adrs-html.sh public/
  artifacts:
    paths:
      - public
```

## Azure DevOps

### Basic Pipeline

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - docs/adr/*

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: Validate
    jobs:
      - job: ValidateADRs
        steps:
          - checkout: self
          - script: |
              for file in docs/adr/[0-9]*.md; do
                echo "Validating $file"
                grep -q "^## Status" "$file" || exit 1
              done
            displayName: 'Validate ADR Format'

  - stage: UpdateIndex
    dependsOn: Validate
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - job: GenerateIndex
        steps:
          - checkout: self
            persistCredentials: true
          - script: ./scripts/generate-adr-index.sh
            displayName: 'Generate Index'
          - script: |
              git config user.email "azure-pipelines@dev.azure.com"
              git config user.name "Azure Pipelines"
              git add docs/adr/README.md
              git diff --staged --quiet || git commit -m "docs(adr): update index [skip ci]"
              git push origin HEAD:main
            displayName: 'Commit Index'
```

## Jenkins

### Jenkinsfile

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Validate ADRs') {
            when {
                changeset "docs/adr/**"
            }
            steps {
                sh '''
                    for file in docs/adr/[0-9]*.md; do
                        echo "Validating $file"
                        grep -q "^## Status" "$file" || exit 1
                        grep -q "^## Context" "$file" || exit 1
                    done
                '''
            }
        }

        stage('Check Compliance') {
            steps {
                sh './scripts/adr-compliance.sh'
            }
        }

        stage('Update Index') {
            when {
                branch 'main'
                changeset "docs/adr/**"
            }
            steps {
                sh './scripts/generate-adr-index.sh'
                sh '''
                    git config user.email "jenkins@company.com"
                    git config user.name "Jenkins"
                    git add docs/adr/README.md
                    git diff --staged --quiet || git commit -m "docs(adr): update index"
                    git push origin main
                '''
            }
        }
    }

    post {
        failure {
            emailext (
                subject: "ADR Validation Failed: ${env.JOB_NAME}",
                body: "Check console output at ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
    }
}
```

## CircleCI

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  validate-adrs:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - run:
          name: Validate ADR Format
          command: |
            for file in docs/adr/[0-9]*.md; do
              grep -q "^## Status" "$file" || exit 1
            done

  update-index:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - run:
          name: Generate Index
          command: ./scripts/generate-adr-index.sh
      - run:
          name: Commit Changes
          command: |
            git config user.email "circleci@company.com"
            git config user.name "CircleCI"
            git add docs/adr/README.md
            git diff --staged --quiet || git commit -m "docs(adr): update index"
            git push origin main

workflows:
  adr-workflow:
    jobs:
      - validate-adrs:
          filters:
            branches:
              only: /.*/
      - update-index:
          requires:
            - validate-adrs
          filters:
            branches:
              only: main
```

## Helper Scripts

### validate-adrs.sh

```bash
#!/bin/bash
# scripts/validate-adrs.sh

set -e
ADR_PATH="${ADR_PATH:-docs/adr}"
ERRORS=0

for file in "$ADR_PATH"/[0-9]*.md; do
    [ -f "$file" ] || continue
    echo "Validating: $file"

    # Check required sections
    if ! grep -q "^## Status" "$file"; then
        echo "  ERROR: Missing Status section"
        ERRORS=$((ERRORS + 1))
    fi

    if ! grep -qE "^## (Context|Context and Problem Statement)" "$file"; then
        echo "  ERROR: Missing Context section"
        ERRORS=$((ERRORS + 1))
    fi

    if ! grep -qE "^## (Decision|Decision Outcome)" "$file"; then
        echo "  ERROR: Missing Decision section"
        ERRORS=$((ERRORS + 1))
    fi

    # Check status value
    STATUS=$(grep -A1 "^## Status" "$file" | tail -1 | tr -d '\n\r ' | tr '[:upper:]' '[:lower:]')
    case "$STATUS" in
        proposed|accepted|deprecated|superseded|rejected) ;;
        *) echo "  WARNING: Unusual status: $STATUS" ;;
    esac
done

if [ $ERRORS -gt 0 ]; then
    echo "Validation failed with $ERRORS errors"
    exit 1
fi

echo "All ADRs validated successfully"
```

### generate-adr-index.sh

```bash
#!/bin/bash
# scripts/generate-adr-index.sh

ADR_PATH="${ADR_PATH:-docs/adr}"
INDEX_FILE="$ADR_PATH/README.md"

cat > "$INDEX_FILE" << 'EOF'
# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for this project.

## What is an ADR?

An ADR is a document that captures an important architectural decision made along with its context and consequences.

## ADR Index

| ID | Title | Status | Date |
|----|-------|--------|------|
EOF

for file in "$ADR_PATH"/[0-9]*.md; do
    [ -f "$file" ] || continue
    BASENAME=$(basename "$file")
    ID=$(echo "$BASENAME" | grep -oE '^[0-9]+')
    TITLE=$(grep -m1 "^# " "$file" | sed 's/^# //' | sed 's/^[0-9]*\. //')
    STATUS=$(grep -A1 "^## Status" "$file" | tail -1 | head -1 | tr -d '\n\r')

    echo "| $ID | [$TITLE](./$BASENAME) | $STATUS | - |" >> "$INDEX_FILE"
done

cat >> "$INDEX_FILE" << 'EOF'

## Status Definitions

| Status | Description |
|--------|-------------|
| Proposed | Under discussion |
| Accepted | Approved and active |
| Deprecated | No longer recommended |
| Superseded | Replaced by another ADR |
| Rejected | Considered but not adopted |

## Creating a New ADR

Use the `/adr-new` command or copy an existing template.
EOF

echo "Index generated: $INDEX_FILE"
```
