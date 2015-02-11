#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>


typedef struct disk_io_file_s          disk_io_file_t;
typedef struct disk_io_file_system_s   disk_io_file_system_t;

struct disk_io_file_s {
    disk_io_file_t          *next_file;
    disk_io_file_system_t   *fs;
    long                     fd;
    long                     offset;
    char                    *buf;
    long                     size;
};

struct disk_io_file_system_s {
    long             file_max_num;
    long             file_num;
    long             fs_pos;
    int              fd;
    disk_io_file_t  *head_file;
};
    



void
disk_io_add_file(disk_io_file_system_t *fs, disk_io_file_t *file)
{
    if (fs->head_file) {
        file->next_file= fs->head_file;
        fs->head_file = file;
    } else {
        fs->head_file = file;
    }
}

void
disk_io_write_file(disk_io_file_system_t *fs, disk_io_file_t *file)
{
    long    ret = 0;

    if ((ret = pwrite(fs->fd, file->buf, file->size, file->offset)) < 0) {
        printf("pwrite error\n");
    }
}

void
disk_io_read_file(disk_io_file_system_t *fs, disk_io_file_t *file)
{
    long ret = 0;

    if ((ret = pread(fs->fd, file->buf, file->size, file->offset)) < 0) {
        printf("pread error\n");
    }
}


int 
main()
{
    char                    buf[101];
    disk_io_file_t         *file = NULL;
    disk_io_file_system_t   fs;
    int                     i = 0;
    
    fs.file_max_num = 10;
    fs.file_num = 0;
    fs.fs_pos = 0;
    fs.head_file = NULL;

    if ((fs.fd = open("/dev/sdb", O_RDWR, 0644)) < 0) {
        printf("open /dev/sdb error\n");
        return -1;
    }

    for (i = 0; i < fs.file_max_num; i++) {
        file = (disk_io_file_t *)malloc(sizeof(disk_io_file_t));

        file->fd = fs.file_num++;
        file->next_file = NULL;
        file->size = 100;
        file->fs = &fs;
        disk_io_add_file(&fs, file);
    }

    file = fs.head_file;
    
    for (i = 0; i < fs.file_num; i++) {
        memset(buf, i + '0', 100);
        buf[100] = '\0';
        file->buf = buf;
        file->offset = fs.fs_pos;
        fs.fs_pos += file->size;
        disk_io_write_file(&fs, file);
        file = file->next_file;
    }

    file = fs.head_file;
    
    for (i = 0; i < fs.file_num; i++) {
        memset(buf, 0, 101);
        file->buf = buf;
        disk_io_read_file(&fs, file);
        printf("%d:%s\n", file->fd, buf);
        file = file->next_file;
    }
    

    close(fs.fd);
}