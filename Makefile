
DUET_WEB_CONTROL ?= "../DuetWebControl"
TARGET_DIR ?= "$(shell pwd)/dist/PrintNannyDuetPlugin"

.PHONY: clean plugin

clean:
	rm -rf $(TARGET_DIR)

$(TARGET_DIR):
	mkdir -p $(TARGET_DIR)

plugin: clean $(TARGET_DIR)
	./tools/duet3d_release.sh
	cd "${DUET_WEB_CONTROL}" && npm run build-plugin "${TARGET_DIR}"
