plugins {
    kotlin("jvm") version "1.8.0"
    `maven-publish`
}

group = "com.displee"
version = "7.3.0"

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib"))
    implementation("com.github.jponge:lzma-java:1.3")
    implementation("org.apache.ant:ant:1.10.14")
    implementation("com.displee:disio:2.2")
}

kotlin {
    jvmToolchain(11)
}

tasks.jar {
    manifest {
        attributes[
            "Implementation-Title"] = "RuneScape Cache Library"
        attributes["Implementation-Version"] = version
    }
}

// Create a fat JAR with all dependencies
tasks.create<Jar>("fatJar") {
    archiveBaseName.set("rs-cache-library")
    archiveClassifier.set("all")
    archiveExtension.set("jar")
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
    manifest {
        attributes["Main-Class"] = "com.displee.cache.CacheLibrary"
    }
    from(configurations.runtimeClasspath.get().map { if (it.isDirectory) it else zipTree(it) })
    with(tasks.jar.get() as CopySpec)
}

publishing {
    publications {
        create<MavenPublication>("maven") {
            groupId = group.toString()
            artifactId = "rs-cache-library"
            version = version

            from(components["java"])
        }
    }
}
