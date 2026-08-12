-- ============================================================
-- TrustLens Database Schema
-- ============================================================

-- ============================================================
-- 1. CONTEXTS
-- ============================================================

CREATE TABLE contexts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    context_type VARCHAR(50) NOT NULL,
    context_name VARCHAR(100) NOT NULL,
    description TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- 2. USERS
-- ============================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    username VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,

    bio TEXT,
    profile_image_url TEXT,

    account_created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================================
-- 3. POSTS
-- ============================================================

CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,
    context_id UUID,

    text TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_posts_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_posts_context
        FOREIGN KEY (context_id)
        REFERENCES contexts(id)
        ON DELETE SET NULL
);


-- ============================================================
-- 4. FOLLOWS
-- ============================================================

CREATE TABLE follows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    follower_id UUID NOT NULL,
    followee_id UUID NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_follows_follower
        FOREIGN KEY (follower_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_follows_followee
        FOREIGN KEY (followee_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT unique_follow_relationship
        UNIQUE (follower_id, followee_id),

    CONSTRAINT no_self_follow
        CHECK (follower_id <> followee_id)
);


-- ============================================================
-- 5. COMMENTS
-- ============================================================

CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,
    post_id UUID NOT NULL,

    text TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_comments_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_comments_post
        FOREIGN KEY (post_id)
        REFERENCES posts(id)
        ON DELETE CASCADE
);


-- ============================================================
-- 6. ATTACKS
-- ============================================================

CREATE TABLE attacks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    attack_type VARCHAR(50) NOT NULL,

    target_user_id UUID,
    target_post_id UUID,

    parameters JSONB,

    status VARCHAR(30) NOT NULL DEFAULT 'completed',

    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_attacks_target_user
        FOREIGN KEY (target_user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_attacks_target_post
        FOREIGN KEY (target_post_id)
        REFERENCES posts(id)
        ON DELETE SET NULL
);


-- ============================================================
-- 7. ATTACK EVENTS
-- ============================================================

CREATE TABLE attack_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    attack_id UUID NOT NULL,

    target_user_id UUID,
    target_post_id UUID,

    event_type VARCHAR(50) NOT NULL,

    metadata JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_attack_events_attack
        FOREIGN KEY (attack_id)
        REFERENCES attacks(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_attack_events_user
        FOREIGN KEY (target_user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_attack_events_post
        FOREIGN KEY (target_post_id)
        REFERENCES posts(id)
        ON DELETE SET NULL
);


-- ============================================================
-- 8. COMMENT DETECTIONS
-- ============================================================

CREATE TABLE comment_detections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    comment_id UUID NOT NULL,

    risk_score NUMERIC(5,2) NOT NULL DEFAULT 0,
    risk_level VARCHAR(20) NOT NULL DEFAULT 'LOW',

    spam_probability NUMERIC(5,4),

    detection_type VARCHAR(100),
    explanation TEXT,

    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_comment_detections_comment
        FOREIGN KEY (comment_id)
        REFERENCES comments(id)
        ON DELETE CASCADE,

    CONSTRAINT unique_comment_detection
        UNIQUE (comment_id)
);


-- ============================================================
-- 9. ACCOUNT DETECTIONS
-- ============================================================

CREATE TABLE account_detections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    risk_score NUMERIC(5,2) NOT NULL DEFAULT 0,
    risk_level VARCHAR(20) NOT NULL DEFAULT 'LOW',

    bot_probability NUMERIC(5,4),

    detection_type VARCHAR(100),
    explanation TEXT,

    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_account_detections_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT unique_account_detection
        UNIQUE (user_id)
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_posts_user_id
    ON posts(user_id);

CREATE INDEX idx_posts_context_id
    ON posts(context_id);

CREATE INDEX idx_posts_created_at
    ON posts(created_at);


CREATE INDEX idx_comments_user_id
    ON comments(user_id);

CREATE INDEX idx_comments_post_id
    ON comments(post_id);

CREATE INDEX idx_comments_created_at
    ON comments(created_at);


CREATE INDEX idx_follows_follower_id
    ON follows(follower_id);

CREATE INDEX idx_follows_followee_id
    ON follows(followee_id);


CREATE INDEX idx_attacks_target_user_id
    ON attacks(target_user_id);

CREATE INDEX idx_attacks_target_post_id
    ON attacks(target_post_id);

CREATE INDEX idx_attacks_created_at
    ON attacks(created_at);


CREATE INDEX idx_attack_events_attack_id
    ON attack_events(attack_id);

CREATE INDEX idx_attack_events_created_at
    ON attack_events(created_at);


CREATE INDEX idx_comment_detections_risk_level
    ON comment_detections(risk_level);

CREATE INDEX idx_account_detections_risk_level
    ON account_detections(risk_level);