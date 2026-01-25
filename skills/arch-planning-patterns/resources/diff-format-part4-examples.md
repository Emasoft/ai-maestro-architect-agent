# Part 4: Examples

**Parent document**: [diff-format.md](diff-format.md)

---

## 4.1 Example 1: Small Diff (1-2 Task Changes)

This example shows a PATCH version increment for minor clarifications.

```markdown
# Plan Diff: API Integration Project
Generated: 2025-01-05T14:30:00Z
From: 1.0.0 → 1.0.1
Author: orchestrator-agent
Reason: Clarified authentication requirements

## Summary
- Phases Added: 0
- Phases Removed: 0
- Phases Modified: 0
- Tasks Added: 0
- Tasks Removed: 0
- Tasks Modified: 2
- Dependencies Added: 0
- Dependencies Removed: 0
- Risks Added: 0
- Risks Removed: 0

## Changes

### Task Changes
~ Modified: [Phase 1] Implement OAuth2 authentication → Implement OAuth2 authentication with PKCE flow
  Changes: Added PKCE (Proof Key for Code Exchange) requirement for enhanced security
  Impact: Requires additional configuration in auth provider settings

~ Modified: [Phase 2] Set up API rate limiting → Set up API rate limiting (100 req/min per user)
  Changes: Added specific rate limit threshold for clarity
  Impact: None - clarification only, original intent unchanged
```

---

## 4.2 Example 2: Medium Diff (Phase Restructure)

This example shows a MAJOR version increment for phase restructuring.

```markdown
# Plan Diff: E-Commerce Platform Rebuild
Generated: 2025-01-05T16:00:00Z
From: 1.2.0 → 2.0.0
Author: orchestrator-agent
Reason: Split monolithic deployment phase into separate infrastructure and application phases

## Summary
- Phases Added: 2
- Phases Removed: 1
- Phases Modified: 1
- Tasks Added: 8
- Tasks Removed: 5
- Tasks Modified: 3
- Dependencies Added: 6
- Dependencies Removed: 4
- Risks Added: 2
- Risks Removed: 1

## Changes

### Phase Changes
- Removed: Phase 4 - Deployment and Launch
  Reason: Too broad, lacked clear separation of concerns

+ Added: Phase 4 - Infrastructure Setup
  Description: Provision cloud resources, configure networking, set up monitoring

+ Added: Phase 5 - Application Deployment
  Description: Deploy services, configure load balancing, run smoke tests

~ Modified: Phase 5 - Post-Launch Monitoring → Phase 6 - Post-Launch Monitoring
  Changes: Renumbered to accommodate new phase structure

### Task Changes
! Breaking: Removed [Phase 4] Deploy all services to production
  Reason: Split into granular infrastructure and deployment tasks
  Impact: Original task was too coarse-grained, new tasks provide better tracking

+ Added: [Phase 4] Provision AWS VPC and subnets
  Dependencies: None
  Success Criteria: VPC created with public/private subnets in 3 AZs

+ Added: [Phase 4] Set up RDS PostgreSQL instances
  Dependencies: "Provision AWS VPC and subnets"
  Success Criteria: Primary and replica databases accessible, backups configured

+ Added: [Phase 4] Configure CloudWatch dashboards
  Dependencies: "Provision AWS VPC and subnets"
  Success Criteria: All infrastructure metrics visible in unified dashboard

+ Added: [Phase 5] Deploy backend API services
  Dependencies: "Set up RDS PostgreSQL instances", "Configure CloudWatch dashboards"
  Success Criteria: All API endpoints responding, health checks passing

+ Added: [Phase 5] Deploy frontend application
  Dependencies: "Deploy backend API services"
  Success Criteria: Frontend accessible, API integration working

+ Added: [Phase 5] Configure Route53 DNS
  Dependencies: "Deploy frontend application"
  Success Criteria: Custom domain pointing to application, SSL certificates valid

+ Added: [Phase 5] Run end-to-end smoke tests
  Dependencies: "Configure Route53 DNS"
  Success Criteria: Critical user flows working in production environment

~ Modified: [Phase 4] Configure monitoring → [Phase 4] Set up application-level monitoring
  Changes: Clarified scope to focus on application metrics (infrastructure monitoring now separate task)
  Impact: Original monitoring task split between Phase 4 (infra) and Phase 5 (app)

### Dependency Changes
+ Added: "Provision AWS VPC and subnets" → "Set up RDS PostgreSQL instances"
  Reason: Database requires VPC networking to be configured first

+ Added: "Set up RDS PostgreSQL instances" → "Deploy backend API services"
  Reason: Backend requires database to be available

+ Added: "Deploy backend API services" → "Deploy frontend application"
  Reason: Frontend depends on backend API endpoints

+ Added: "Deploy frontend application" → "Run end-to-end smoke tests"
  Reason: Can only test after full deployment complete

- Removed: "Complete testing" → "Deploy all services"
  Reason: Original dependency obsolete due to phase restructure

### Risk Changes
+ Added: [HIGH] Infrastructure provisioning may take longer than estimated
  Mitigation: Start infrastructure setup early, use Infrastructure-as-Code for repeatability

+ Added: [MEDIUM] Database migration may encounter issues in production
  Mitigation: Test migration on production-like staging environment first

- Removed: [LOW] Deployment script may fail
  Reason: Now using robust CI/CD pipeline instead of manual scripts
```

---

## 4.3 Example 3: Large Diff (Major Replanning)

This example shows a complete technology pivot requiring extensive changes.

```markdown
# Plan Diff: Mobile App Development
Generated: 2025-01-06T09:00:00Z
From: 2.1.0 → 3.0.0
Author: orchestrator-agent
Reason: Major pivot from native iOS/Android to React Native cross-platform approach

## Summary
- Phases Added: 3
- Phases Removed: 4
- Phases Modified: 2
- Tasks Added: 15
- Tasks Removed: 22
- Tasks Modified: 7
- Dependencies Added: 18
- Dependencies Removed: 25
- Risks Added: 4
- Risks Removed: 3

## Changes

### Phase Changes
! Breaking: Removed Phase 1 - iOS Development
  Reason: Switching to React Native eliminates need for separate iOS development
  Impact: All iOS-specific work invalidated, team needs React Native training

! Breaking: Removed Phase 2 - Android Development
  Reason: Switching to React Native eliminates need for separate Android development
  Impact: All Android-specific work invalidated

! Breaking: Removed Phase 3 - iOS/Android Feature Parity
  Reason: React Native ensures feature parity by default
  Impact: Eliminates entire phase of work

! Breaking: Removed Phase 4 - Platform-Specific Testing
  Reason: Consolidated into unified cross-platform testing
  Impact: Reduces testing complexity

+ Added: Phase 1 - React Native Setup
  Description: Configure React Native environment, set up navigation, establish component library

+ Added: Phase 2 - Core Feature Development
  Description: Implement authentication, data sync, offline support, push notifications

+ Added: Phase 3 - Platform Optimization
  Description: Optimize performance, add platform-specific polish, test on real devices

~ Modified: Phase 5 - App Store Deployment → Phase 4 - App Store Deployment
  Changes: Renumbered and updated for simultaneous iOS/Android release

~ Modified: Phase 6 - Post-Launch Support → Phase 5 - Post-Launch Support
  Changes: Renumbered only

### Task Changes
! Breaking: Removed [Phase 1] Implement iOS authentication with Sign in with Apple
  Reason: Replaced by unified React Native authentication
  Impact: Work not started yet, no loss

! Breaking: Removed [Phase 2] Implement Android authentication with Google Sign-In
  Reason: Replaced by unified React Native authentication
  Impact: Work not started yet, no loss

+ Added: [Phase 1] Initialize React Native project with TypeScript
  Dependencies: None
  Success Criteria: Project builds successfully for both iOS and Android

+ Added: [Phase 1] Set up React Navigation v6
  Dependencies: "Initialize React Native project with TypeScript"
  Success Criteria: Tab and stack navigation working, deep linking configured

+ Added: [Phase 1] Create design system component library
  Dependencies: "Initialize React Native project with TypeScript"
  Success Criteria: Reusable button, input, card components with consistent styling

+ Added: [Phase 2] Implement unified authentication
  Dependencies: "Set up React Navigation v6", "Create design system component library"
  Success Criteria: OAuth2 login working on both platforms

+ Added: [Phase 2] Build offline-first data layer
  Dependencies: "Implement unified authentication"
  Success Criteria: App functions offline, syncs when connectivity restored

+ Added: [Phase 2] Integrate push notifications
  Dependencies: "Implement unified authentication"
  Success Criteria: Push notifications received on both iOS and Android

+ Added: [Phase 3] Optimize React Native performance
  Dependencies: "Build offline-first data layer", "Integrate push notifications"
  Success Criteria: App startup under 2 seconds, smooth 60fps animations

+ Added: [Phase 3] Add platform-specific polish
  Dependencies: "Optimize React Native performance"
  Success Criteria: Native feel on both platforms (haptics, gestures, transitions)

+ Added: [Phase 3] Conduct cross-platform testing
  Dependencies: "Add platform-specific polish"
  Success Criteria: All tests pass on iOS 15+, Android 10+

~ Modified: [Phase 5] Submit to App Store → [Phase 4] Submit to both App Store and Google Play simultaneously
  Changes: Updated for simultaneous dual-platform release
  Impact: Requires parallel app store preparation workflows

### Dependency Changes
! Breaking: Removed all iOS-specific → Android-specific dependencies
  Reason: No longer maintaining separate codebases
  Impact: Entire dependency graph restructured

+ Added: "Initialize React Native project" → "Set up React Navigation v6"
  Reason: Navigation depends on base project setup

+ Added: "Create design system" → "Implement unified authentication"
  Reason: Auth UI uses design system components

+ Added: "Implement unified authentication" → "Build offline-first data layer"
  Reason: Data sync requires authenticated user context

+ Added: "Build offline-first data layer" → "Optimize React Native performance"
  Reason: Performance optimization after features complete

### Risk Changes
! Breaking: Removed [HIGH] iOS and Android features drift out of sync
  Reason: No longer applicable with shared React Native codebase

+ Added: [HIGH] Team lacks React Native experience
  Mitigation: Allocate 2 weeks for training, hire React Native consultant for first sprint

+ Added: [MEDIUM] React Native performance may not match native apps
  Mitigation: Profile performance early, use native modules for critical paths if needed

+ Added: [MEDIUM] Third-party React Native libraries may lack quality
  Mitigation: Evaluate libraries carefully, maintain fork if necessary, contribute fixes upstream

+ Added: [LOW] React Native version upgrades may break dependencies
  Mitigation: Pin versions, test upgrades in separate branch, follow React Native upgrade helper

### Success Criteria Changes
~ Modified: "iOS app passes App Store review" → "Both iOS and Android apps pass store reviews"
  Reason: Now targeting simultaneous release on both platforms

~ Modified: "Feature parity achieved between platforms" → "Single codebase supports both platforms"
  Reason: React Native ensures parity by default

### Milestone Changes
- Removed: "iOS Beta Release" - 2025-02-15
  Reason: No longer doing separate iOS development

- Removed: "Android Beta Release" - 2025-03-01
  Reason: No longer doing separate Android development

+ Added: "Cross-Platform Beta Release" - 2025-02-20
  Success Criteria: App runs on both iOS and Android test devices, core features working

~ Modified: "Public Launch" - 2025-04-01 → 2025-03-15
  Reason: React Native approach reduces development time by 6 weeks
```

---

**Previous**: [Part 3: Tooling Integration](diff-format-part3-tooling.md)

**Next**: [Part 5: Best Practices and Troubleshooting](diff-format-part5-best-practices.md)
