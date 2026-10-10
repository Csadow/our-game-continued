cmake_minimum_required(VERSION 3.16)
project(OrbitBulletHell LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(OpenGL REQUIRED)
find_package(glfw3 3.3 REQUIRED)
find_package(GLEW REQUIRED)
find_package(glm CONFIG REQUIRED)

add_executable(bullethell main.cpp game.cpp)
target_link_libraries(bullethell PRIVATE OpenGL::GL glfw GLEW::GLEW glm::glm)
if(MSVC)
    target_compile_options(bullethell PRIVATE /W4)
else()
    target_compile_options(bullethell PRIVATE -Wall -Wextra -Wpedantic)
endif()

# Keep the executable and shaders together, including with multi-config generators.
set_target_properties(bullethell PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")
foreach(config DEBUG RELEASE RELWITHDEBINFO MINSIZEREL)
    set_target_properties(bullethell PROPERTIES RUNTIME_OUTPUT_DIRECTORY_${config} "${CMAKE_BINARY_DIR}")
endforeach()
foreach(shader scene.vert scene.frag hud.vert hud.frag)
    configure_file("${shader}" "${CMAKE_BINARY_DIR}/${shader}" COPYONLY)
endforeach()

# Allow launching the MinGW build from Explorer as well as the MSYS2 terminal.
if(WIN32 AND MINGW)
    get_filename_component(mingw_bin "${CMAKE_CXX_COMPILER}" DIRECTORY)
    foreach(dll glfw3.dll glew32.dll libstdc++-6.dll libgcc_s_seh-1.dll libwinpthread-1.dll)
        if(EXISTS "${mingw_bin}/${dll}")
            add_custom_command(TARGET bullethell POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy_if_different
                    "${mingw_bin}/${dll}" "$<TARGET_FILE_DIR:bullethell>/${dll}")
        endif()
    endforeach()
endif()

