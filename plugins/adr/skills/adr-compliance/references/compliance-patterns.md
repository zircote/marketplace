# ADR Compliance Patterns

Common patterns for checking code compliance with Architectural Decision Records.

## Technology Selection Compliance

### Database Technology Checks

**ADR Type**: "Use {database} for data storage"

**Grep Patterns**:
```bash
# PostgreSQL compliance (should find)
grep -r "pg\|postgres\|psycopg\|node-postgres" src/

# MySQL violation detection (should not find)
grep -r "mysql\|mysql2\|pymysql" src/

# MongoDB violation detection
grep -r "mongoose\|mongodb\|pymongo" src/
```

**Import Patterns**:
```typescript
// Compliant
import { Pool } from 'pg';
import postgres from 'postgres';

// Violation
import mysql from 'mysql2';
import { MongoClient } from 'mongodb';
```

### Message Queue Checks

**ADR Type**: "Use {queue} for async messaging"

**Patterns for Kafka compliance**:
```bash
# Should find Kafka usage
grep -r "kafkajs\|node-rdkafka\|kafka-python" src/

# Should NOT find alternatives
grep -r "amqplib\|rabbitmq\|bullmq\|aws-sdk.*sqs" src/
```

### Cache Technology Checks

**ADR Type**: "Use Redis for caching"

```bash
# Should find Redis
grep -r "redis\|ioredis\|redis-py" src/

# Should NOT find alternatives
grep -r "memcached\|node-cache\|lru-cache" src/
```

## Pattern Adoption Compliance

### Event-Driven Architecture

**ADR Type**: "Adopt event-driven architecture"

**Compliance indicators**:
```bash
# Event publishing (good)
grep -r "emit\|publish\|dispatch.*event\|EventEmitter" src/

# Direct service calls (potential violation)
grep -r "fetch\|axios\|http\.request" src/services/
```

**Code structure checks**:
```typescript
// Compliant - event-based communication
eventBus.publish('OrderCreated', order);
await eventEmitter.emit('PaymentProcessed', payment);

// Violation - direct synchronous call
const result = await paymentService.process(order);
const user = await userService.getById(userId);
```

### Microservices Boundaries

**ADR Type**: "Services must not share databases"

```bash
# Check for cross-service database imports
# Each service should only import its own db config
grep -r "import.*from.*other-service.*db" src/
```

### API Design Patterns

**ADR Type**: "Use REST conventions for APIs"

```bash
# Should find RESTful patterns
grep -r "@Get\|@Post\|@Put\|@Delete\|router\.(get|post|put|delete)" src/

# GraphQL usage (violation if REST mandated)
grep -r "graphql\|@Query\|@Mutation\|gql\`" src/
```

## Constraint Compliance

### Authentication Requirements

**ADR Type**: "All external APIs must require authentication"

**Check for unprotected endpoints**:
```bash
# Find route definitions
grep -rn "router\.\(get\|post\|put\|delete\)" src/routes/

# Check each has auth middleware
grep -B2 "router\.\(get\|post\|put\|delete\)" src/routes/ | grep -v "authMiddleware\|requireAuth\|@Authorized"
```

**Decorator/middleware patterns**:
```typescript
// Compliant
@UseGuards(AuthGuard)
@Get('users')
async getUsers() {}

// Violation - no auth guard
@Get('public-data')
async getPublicData() {}
```

### Input Validation

**ADR Type**: "All API inputs must be validated"

```bash
# Check for validation decorators/middleware
grep -r "@IsString\|@IsNumber\|@ValidateNested\|Joi\.object\|zod\.object" src/

# Find endpoints without validation
grep -rn "@Body()\|req\.body" src/ | grep -v "ValidationPipe\|validate"
```

### Error Handling

**ADR Type**: "Use structured error responses"

```bash
# Check for consistent error patterns
grep -r "throw new.*Error\|res\.status.*json" src/

# Look for raw throws without wrapping
grep -r "throw new Error\(" src/ | grep -v "AppError\|HttpException\|ApiError"
```

## Security Compliance

### Secrets Management

**ADR Type**: "No hardcoded secrets"

```bash
# Check for potential hardcoded secrets
grep -rn "password\s*=\s*['\"]" src/
grep -rn "api[_-]?key\s*=\s*['\"]" src/
grep -rn "secret\s*=\s*['\"]" src/

# Should use environment variables
grep -r "process\.env\.\|os\.environ\|config\." src/
```

### SQL Injection Prevention

**ADR Type**: "Use parameterized queries"

```bash
# Potential SQL injection (string concatenation)
grep -rn "query.*\+.*\+" src/
grep -rn "execute.*f['\"]" src/  # Python f-strings in queries

# Compliant patterns
grep -r "\$1\|\$2\|:param\|?" src/  # Parameterized placeholders
```

### CORS Configuration

**ADR Type**: "Restrict CORS to approved origins"

```bash
# Check for overly permissive CORS
grep -r "origin:\s*['\"]?\*['\"]?" src/
grep -r "Access-Control-Allow-Origin.*\*" src/
```

## Architecture Layer Compliance

### Layer Dependency Rules

**ADR Type**: "Controllers must not directly access repositories"

```bash
# Controllers should use services, not repositories
grep -r "import.*Repository" src/controllers/

# Services can use repositories (compliant)
grep -r "import.*Repository" src/services/
```

### Import Path Rules

```bash
# Check for violations of layer boundaries
# UI should not import from data layer
grep -r "import.*from.*data\|import.*from.*repository" src/ui/

# Domain should not import from infrastructure
grep -r "import.*from.*infrastructure" src/domain/
```

## Compliance Report Generation

### Summary Template

```markdown
## ADR Compliance Check Results

**Date**: {date}
**Commit**: {commit_hash}
**Files Scanned**: {count}

### Summary

| ADR | Status | Violations |
|-----|--------|------------|
| ADR-001 | ✅ Compliant | 0 |
| ADR-002 | ⚠️ Warning | 2 |
| ADR-003 | ❌ Violation | 5 |

### Violations Detail

#### ADR-002: Use PostgreSQL

**Warning**: Found potential MySQL imports
- `src/legacy/data.js:45` - `require('mysql')`
- `src/migrations/old.js:12` - `import mysql from 'mysql2'`

**Recommendation**: Migrate legacy code to PostgreSQL
```

## Automated Compliance Scripts

### Basic Compliance Checker

```bash
#!/bin/bash
# compliance-check.sh

VIOLATIONS=0

echo "Checking ADR-001: PostgreSQL Usage"
if grep -rq "mysql\|mongodb" src/; then
    echo "❌ VIOLATION: Non-PostgreSQL database found"
    VIOLATIONS=$((VIOLATIONS + 1))
else
    echo "✅ Compliant"
fi

echo "Checking ADR-002: Event-Driven Architecture"
if grep -rq "direct.*service.*call" src/services/; then
    echo "⚠️ WARNING: Direct service calls found"
fi

exit $VIOLATIONS
```

### CI Integration

```yaml
# GitHub Actions example
- name: ADR Compliance Check
  run: |
    ./scripts/compliance-check.sh
  continue-on-error: false
```
