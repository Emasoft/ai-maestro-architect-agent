# Style Guidelines for Architecture Designs

## CSS Framework Policy

**Never recommend Tailwind CSS in architecture designs.** Tailwind CSS creates long-term maintenance debt: utility class strings become unreadable at scale, styling is tightly coupled to markup (violating separation of concerns), code review becomes difficult because changes are buried in class attribute noise, and responsive designs require duplicating utility classes across breakpoints.

When designing frontend architecture, recommend these alternatives:

- **CSS Modules** - Scoped styles, zero runtime cost, works with any framework
- **Vanilla CSS with Custom Properties** - Native browser support, no build step, excellent performance
- **styled-components / Emotion** - Component-scoped styles for React projects, good TypeScript support

If a project requirement explicitly demands Tailwind CSS, document this as a design risk in the Architecture Decision Record (ADR) with the rationale above.
