# Requirements Document

## Introduction

The current AlgoTradeHub application runs on two separate ports - a Flask backend on port 5000 and a Next.js frontend on port 3000. This creates confusion for users and unnecessary complexity in deployment and development. This feature will consolidate the entire application to run exclusively on port 3000, eliminating the need for the separate Flask backend server.

## Requirements

### Requirement 1

**User Story:** As a developer, I want to run only one application server, so that I can simplify development and deployment processes.

#### Acceptance Criteria

1. WHEN the application starts THEN only port 3000 SHALL be used
2. WHEN a user accesses the application THEN all functionality SHALL be available through port 3000
3. WHEN the system is deployed THEN only one server process SHALL be required

### Requirement 2

**User Story:** As a user, I want all application features accessible from a single URL, so that I don't need to remember multiple ports or endpoints.

#### Acceptance Criteria

1. WHEN accessing trading features THEN they SHALL be available at localhost:3000/trading
2. WHEN accessing portfolio features THEN they SHALL be available at localhost:3000/portfolio
3. WHEN accessing exchange configuration THEN it SHALL be available at localhost:3000/exchanges
4. WHEN making API calls THEN they SHALL all go through port 3000 endpoints

### Requirement 3

**User Story:** As a system administrator, I want simplified deployment architecture, so that I can reduce infrastructure complexity and maintenance overhead.

#### Acceptance Criteria

1. WHEN deploying the application THEN only Next.js server SHALL be required
2. WHEN configuring reverse proxy THEN only port 3000 SHALL need to be exposed
3. WHEN monitoring the system THEN only one application process SHALL need to be tracked

### Requirement 4

**User Story:** As a developer, I want all backend functionality integrated into Next.js API routes, so that I can maintain a single codebase and deployment pipeline.

#### Acceptance Criteria

1. WHEN backend logic is needed THEN it SHALL be implemented as Next.js API routes
2. WHEN Python functionality is required THEN it SHALL be called from Next.js API routes
3. WHEN database operations are needed THEN they SHALL be handled through Next.js middleware
4. WHEN external APIs are called THEN they SHALL be proxied through Next.js API routes

### Requirement 5

**User Story:** As a user, I want seamless functionality without knowing about backend architecture, so that I can focus on trading activities rather than technical details.

#### Acceptance Criteria

1. WHEN using trading features THEN response times SHALL be equivalent to current performance
2. WHEN switching between pages THEN navigation SHALL be instant without external redirects
3. WHEN errors occur THEN they SHALL be handled gracefully within the single application
4. WHEN real-time data is needed THEN it SHALL be delivered through the same port 3000 connection