# XML Demarcation Templates

Reference templates for consistent XML usage across marketplace plugins.

## Command Templates

### Step Structure
```xml
<step number="N" name="description">
  <action>What to do</action>
  <verification>How to verify success</verification>
  <error_handling>
    <error type="type_name" severity="HIGH|MEDIUM|LOW">
      <condition>When this fails</condition>
      <recovery>How to fix</recovery>
    </error>
  </error_handling>
</step>
```

### Phase Structure
```xml
<phase number="N" name="Phase Name">
  <objective>What this phase accomplishes</objective>
  <steps>
    <!-- Step tags go here -->
  </steps>
  <success_criteria>How to know phase is complete</success_criteria>
</phase>
```

### Conditional Logic
```xml
<conditional id="unique_id">
  <condition>When X is true</condition>
  <then>Do A</then>
  <else>Do B</else>
</conditional>
```

### Error Handling Section
```xml
<error_handling>
  <error type="git_failure" severity="HIGH">
    <condition>When git command fails</condition>
    <message>Display to user</message>
    <recovery>How to fix it</recovery>
  </error>
  <error type="api_timeout" severity="MEDIUM">
    <condition>When API call times out</condition>
    <message>API request timed out</message>
    <recovery>Retry with backoff</recovery>
  </error>
</error_handling>
```

### User Interaction
```xml
<ask_user_question id="scope_selection">
  <trigger>After discovery phase</trigger>
  <header>Scope</header>
  <question>What should I review?</question>
  <multiSelect>false</multiSelect>
  <options>
    <option label="Option A">Description A</option>
    <option label="Option B">Description B</option>
  </options>
</ask_user_question>
```

### Workflow Structure
```xml
<workflow name="workflow_name">
  <preflight_checks>
    <check name="branch_check">Verify on correct branch</check>
    <check name="clean_state">Verify no uncommitted changes</check>
  </preflight_checks>
  <steps>
    <!-- Step tags go here -->
  </steps>
  <completion>
    <success_message>Workflow completed successfully</success_message>
    <artifacts>List of created/modified files</artifacts>
  </completion>
</workflow>
```

## Agent Templates

### Deliberate Protocol
```xml
<deliberate_protocol name="domain_name">
  <enforcement_rules>
    <rule sequence="1">
      <condition>Before action X</condition>
      <action>Verification action</action>
      <validation>Cross-reference method</validation>
    </rule>
    <rule sequence="2">
      <condition>Before action Y</condition>
      <action>Another verification</action>
      <validation>Validation method</validation>
    </rule>
  </enforcement_rules>
</deliberate_protocol>
```

### Execution Strategy
```xml
<execution_strategy>
  <parallel>
    <operation priority="1">Read multiple files simultaneously</operation>
    <operation priority="2">Fetch documentation and templates together</operation>
    <operation priority="3">Run tests across multiple targets</operation>
  </parallel>
  <sequential>
    <constraint sequence="1">
      <condition>X depends on Y analysis</condition>
      <impact>Must complete Y before X</impact>
    </constraint>
    <constraint sequence="2">
      <condition>Setup must precede implementation</condition>
      <impact>State structure must be finalized first</impact>
    </constraint>
  </sequential>
</execution_strategy>
```

### Checklist
```xml
<checklist type="checklist_type" validation_required="true">
  <item priority="critical" domain="domain_name">
    <criterion>What to check</criterion>
    <validation_method>How to validate</validation_method>
    <failure_impact>What happens if this fails</failure_impact>
  </item>
  <item priority="high" domain="domain_name">
    <criterion>Another criterion</criterion>
    <validation_method>Validation approach</validation_method>
    <failure_impact>Impact description</failure_impact>
  </item>
</checklist>
```

### Output Format
```xml
<output_format type="completion_notification">
  <template>
    <opening_statement>Deliverable type delivered successfully</opening_statement>
    <key_artifacts>
      <artifact type="module" location="/path/to/artifact">
        <features>
          <feature>Feature 1</feature>
          <feature>Feature 2</feature>
        </features>
      </artifact>
    </key_artifacts>
    <readiness_status>Ready for next step</readiness_status>
  </template>
</output_format>
```

### Conditional Requirements
```xml
<conditional_requirements>
  <mcp_tool name="tool_name" required="true">
    <purpose>What it does</purpose>
    <requires_plugin>Plugin name</requires_plugin>
    <fallback>Alternative if unavailable</fallback>
  </mcp_tool>
</conditional_requirements>
```

## Skill Templates

### Example Wrapper
```xml
<example type="good|bad" domain="security|performance|etc">
  <scenario>Context for this example</scenario>
  <code language="typescript">
    // Example code here
  </code>
  <explanation>Why this is good/bad</explanation>
</example>
```

### Constraints Section
```xml
<constraints>
  <constraint severity="blocking">Hard limitation that prevents action</constraint>
  <constraint severity="warning">Soft limitation to be aware of</constraint>
  <constraint severity="info">Informational limitation</constraint>
</constraints>
```

### Output Template
```xml
<output_template name="template_name">
  <format>JSON|Markdown|Plain</format>
  <structure>
    Expected structure description
  </structure>
  <example>
    Concrete example of expected output
  </example>
</output_template>
```

### Triggers
```xml
<triggers>
  <trigger>When user mentions X</trigger>
  <trigger>When working on Y</trigger>
  <trigger>When file pattern Z detected</trigger>
</triggers>
```

### Configuration Section
```xml
<configuration>
  <step number="1">Description of setup step</step>
  <config_block type="env">
    Environment variables or config values
  </config_block>
  <verification>How to verify configuration is correct</verification>
</configuration>
```
